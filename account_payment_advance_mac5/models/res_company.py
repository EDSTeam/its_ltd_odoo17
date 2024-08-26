from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    advance_payment_account_id = fields.Many2one(
        'account.account',
        string="Incoming Advance Payment Account",
        help="The account must be reconcilable"
    )
    advance_payment_outgoing_account_id = fields.Many2one(
        'account.account',
        string="Outgoing Advance Payment Account",
        help="The account must be reconcilable"
    )
    advance_payment_journal_id = fields.Many2one(
        'account.journal',
        string="Default Advance Payment Journal",
        help="Default advance payment journal for the current user's company."
    )
