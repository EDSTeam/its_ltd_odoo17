# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api


class ShProductTemplate(models.Model):
    _inherit = 'product.template'

    sh_bundle_product_ids = fields.One2many(
        'sh.product.bundle', 'sh_bundle_id', string="Bundle Line")
    sh_is_bundle = fields.Boolean('Is Bundled ?')
    sh_amount_total = fields.Monetary(
        string='Total', store=True, readonly=True, compute='_amount_all')

    @api.depends('sh_bundle_product_ids.sh_price_subtotal')
    def _amount_all(self):
        amount_total = 0.0
        for order in self:
            if order.sh_bundle_product_ids:
                for line in self.sh_bundle_product_ids:
                    amount_total += line.sh_price_subtotal
                order.sh_amount_total = amount_total
            else:
                order.sh_amount_total = amount_total


class ShBundleProduct(models.Model):
    _name = 'sh.product.bundle'
    _description = 'Bundle Products'

    sh_bundle_id = fields.Many2one('product.template', 'Bundle ID')
    sh_product_id = fields.Many2one(
        'product.product', 'Product', required=True)
    sh_qty = fields.Float("Quantity")
    sh_uom = fields.Many2one('uom.uom', 'Unit of Measure')
    sh_price_unit = fields.Float('Unit Price')
    sh_price_subtotal = fields.Float('Sub Total', readonly=True, store=True)

    @api.onchange('sh_product_id')
    def _onchange_sh_product_id(self):
        if self.sh_product_id:
            self.sh_uom = self.sh_product_id.uom_id.id
            self.sh_qty = 1.0

    @api.onchange('sh_qty', 'sh_price_unit')
    def get_price_subtotal(self):
        for rec in self:
            rec.sh_price_subtotal = rec.sh_price_unit * rec.sh_qty
