from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_advance_payment = fields.Boolean('Advance Payment?', default=False)
    advance_payment_account_id = fields.Many2one('account.account', 'Advance Payment Account')
    residual = fields.Monetary(string='Remaining Amount', compute='_compute_residual',
                               readonly=True, store=True, help="Remaining amount to apply.")
    move_line_ids = fields.One2many('account.move.line', 'payment_id', readonly=True)
    move_reconciled = fields.Boolean(compute="_compute_move_reconciled", readonly=True)

    @api.depends('advance_payment_account_id')
    def _compute_destination_account_id(self):
        super(AccountPayment, self)._compute_destination_account_id()
        for payment in self:
            if (payment.payment_type != 'transfer' and payment.is_advance_payment
                    and payment.advance_payment_account_id):
                payment.destination_account_id = payment.advance_payment_account_id.id

    @api.depends('is_advance_payment')
    def _compute_partner_id(self):
        super(AccountPayment, (self.filtered(lambda x: not x.is_advance_payment)))._compute_partner_id()

    @api.depends('amount', 'currency_id', 'move_line_ids', 'move_line_ids.reconciled',
                 'move_line_ids.matched_debit_ids', 'move_line_ids.matched_credit_ids')
    def _compute_residual(self):
        reconciled_payment = self.filtered('move_reconciled')
        reconciled_payment.update({'residual': 0.0})
        for payment in (self - reconciled_payment):
            residual = payment.amount
            invoice_lines = (payment.move_line_ids.mapped('matched_debit_ids.debit_move_id')
                             + payment.move_line_ids.mapped('matched_credit_ids.credit_move_id'))
            for line in invoice_lines.filtered('is_advance_payment_account'):
                line_currency = line.currency_id or line.company_id.currency_id
                line_currency = line_currency.with_context(date=payment.date)
                if line.currency_id:
                    line_amount = abs(line.amount_currency)
                else:
                    line_amount = abs(line.credit - line.debit)
                if payment.currency_id != line_currency:
                    residual -= line_currency._convert(line_amount, payment.currency_id)
                else:
                    residual -= line_amount
            payment.residual = residual

    @api.depends('move_line_ids.reconciled')
    def _compute_move_reconciled(self):
        for payment in self:
            rec = True
            for aml in payment.move_line_ids.filtered(lambda x: x.account_id.reconcile):
                if not aml.reconciled:
                    rec = False
                    break
            payment.move_reconciled = rec

    @api.onchange('journal_id', 'payment_type')
    def _onchange_journal_payment_type(self):
        company = self.journal_id.company_id
        self.company_id = company.id
        if self.payment_type == 'inbound':
            self.advance_payment_account_id = company.advance_payment_account_id.id
        else:
            self.advance_payment_account_id = company.advance_payment_outgoing_account_id.id
        self.is_advance_payment = self.env.context.get('default_is_advance_payment', False)

    def _seek_for_lines(self):
        liquidity_lines, counterpart_lines, writeoff_lines = super()._seek_for_lines()

        if not counterpart_lines and writeoff_lines:
            advance_payment_lines = writeoff_lines.filtered(lambda l: l.account_id.used_for_advance_payment and l.account_id.reconcile)
            if advance_payment_lines:
                counterpart_lines += advance_payment_lines
                writeoff_lines -= advance_payment_lines

        if self.is_advance_payment and self.destination_account_id == self.advance_payment_account_id:
            counterpart_lines.is_advance_payment_account = True
        else:
            counterpart_lines.is_advance_payment_account = False
        return liquidity_lines, counterpart_lines, writeoff_lines
