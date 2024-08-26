from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    advance_payment_account_id = fields.Many2one(
        related='company_id.advance_payment_account_id',
        readonly=False
    )
    advance_payment_outgoing_account_id = fields.Many2one(
        related='company_id.advance_payment_outgoing_account_id',
        readonly=False
    )
    advance_payment_journal_id = fields.Many2one(
        related='company_id.advance_payment_journal_id',
        readonly=False
    )
