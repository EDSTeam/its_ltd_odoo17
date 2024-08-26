# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ResCompanyInherit(models.Model):
    _inherit = "res.company"

    sh_po_sub_merge_qty = fields.Boolean(string="Subtract Merged Quantity")


class ResConfigSettingsInherit(models.TransientModel):
    _inherit = "res.config.settings"

    sh_po_sub_merge_qty = fields.Boolean(related="company_id.sh_po_sub_merge_qty", string="Subtract Merged Quantity", readonly=False)
