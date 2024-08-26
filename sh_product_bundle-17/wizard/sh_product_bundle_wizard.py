# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api


class ShProductBundleWizard(models.TransientModel):
    _name = 'sh.product.bundle.wizard'
    _description = 'Bundle Wizard'

    sh_partner_id = fields.Many2one('res.partner', 'Customer', required=True)
    sh_bundle_id = fields.Many2one(
        'product.template', 'Add Pack / Bundle', required=True, domain=[('sh_is_bundle', '=', True)])
    sh_qty = fields.Float('Quantity', default=1.00, required=True)
    sh_price = fields.Float('Pack / Bundle Price')
    sh_bundle_lines = fields.One2many(
        'sh.product.bundle.wizard.line', 'wizard_id', string='Bundle Lines')

    @api.onchange('sh_qty')
    def onchange_bundle_line(self):
        self.sh_price = self.sh_bundle_id.list_price * self.sh_qty
        if self.sh_bundle_id and self.sh_bundle_id.sh_bundle_product_ids:
            line_ids = []
            if self.sh_bundle_lines:
                self.sh_bundle_lines = False
                for line in self.sh_bundle_id.sh_bundle_product_ids:
                    line_vals = {
                        'sh_product_id': line.sh_product_id.id,
                        'sh_bundle_quantity': line.sh_qty * self.sh_qty,
                        'sh_bundle_uom': line.sh_uom.id,
                    }
                    line_ids.append((0, 0, line_vals))
                self.sh_bundle_lines = line_ids
            else:
                for line in self.sh_bundle_id.sh_bundle_product_ids:
                    line_vals = {
                        'sh_product_id': line.sh_product_id.id,
                        'sh_bundle_quantity': line.sh_qty * self.sh_qty,
                        'sh_bundle_uom': line.sh_uom.id,
                    }
                    line_ids.append((0, 0, line_vals))
                self.sh_bundle_lines = line_ids

    @api.onchange('sh_bundle_id')
    def onchange_bundle(self):
        if self.sh_bundle_id:
            if self.sh_bundle_id and self.sh_bundle_id.sh_bundle_product_ids:
                if self.sh_bundle_lines:
                    self.sh_bundle_lines = False
                    line_ids = []
                    self.sh_price = self.sh_bundle_id.list_price
                    for line in self.sh_bundle_id.sh_bundle_product_ids:
                        line_vals = {
                            'sh_product_id': line.sh_product_id.id,
                            'sh_bundle_quantity': line.sh_qty,
                            'sh_bundle_uom': line.sh_uom.id,
                        }
                        line_ids.append((0, 0, line_vals))
                    self.sh_bundle_lines = line_ids
                else:
                    line_ids = []
                    self.sh_price = self.sh_bundle_id.sh_amount_total
                    for line in self.sh_bundle_id.sh_bundle_product_ids:
                        line_vals = {
                            'sh_product_id': line.sh_product_id.id,
                            'sh_bundle_quantity': line.sh_qty,
                            'sh_bundle_uom': line.sh_uom.id,
                        }
                        line_ids.append((0, 0, line_vals))
                    self.sh_bundle_lines = line_ids

    def action_add_pack(self):
        context = self.env.context
        if context.get('active_model') == 'sale.order':
            sale_order = self.env['sale.order'].sudo().search(
                [('id', '=', context.get('active_id'))], limit=1)
            if sale_order and self.sh_bundle_lines:
                product_lines = []
                line_vals = {}
                line_vals = {
                    'order_id': sale_order.id,
                    'product_id': self.sh_bundle_id.product_variant_id.id,
                    'name': self.sh_bundle_id.product_variant_id.name,
                    'product_uom': self.sh_bundle_id.product_variant_id.uom_id.id,
                    'product_uom_qty': self.sh_qty,
                    'price_unit': self.sh_bundle_id.list_price,
                }
                product_lines.append((0, 0, line_vals))
                for line in self.sh_bundle_lines:
                    product_line_vals = {
                        'order_id': sale_order.id,
                        'product_id': line.sh_product_id.id,
                        'name': line.sh_product_id.name,
                        'product_uom': line.sh_bundle_uom.id,
                        'product_uom_qty': line.sh_bundle_quantity,
                        'price_unit': 0.0,
                    }
                    product_lines.append((0, 0, product_line_vals))
                sale_order.order_line = product_lines
        elif context.get('active_model') == 'stock.picking':
            picking_id = self.env['stock.picking'].sudo().search(
                [('id', '=', context.get('active_id'))], limit=1)
            src_location = None
            dest_location = None
            if picking_id.picking_type_code == 'incoming':
                src_location = self.env.ref('stock.stock_location_suppliers')
                dest_location = self.env.ref('stock.stock_location_stock')
            elif picking_id.picking_type_code == 'outgoing':
                src_location = self.env.ref('stock.stock_location_stock')
                dest_location = self.env.ref('stock.stock_location_customers')
            elif picking_id.picking_type_code == 'internal':
                src_location = picking_id.location_id
                dest_location = picking_id.location_dest_id
            if picking_id and self.sh_bundle_lines:
                product_lines = []
                line_vals = {}
                line_vals = {
                    'picking_id': picking_id.id,
                    'name': self.sh_bundle_id.product_variant_id.name,
                    'location_id': src_location.id,
                    'location_dest_id': dest_location.id,
                    'product_id': self.sh_bundle_id.product_variant_id.id,
                    'product_uom': self.sh_bundle_id.product_variant_id.uom_id.id,
                    'product_uom_qty': self.sh_qty,
                    'state': 'draft',
                }
                product_lines.append((0, 0, line_vals))
                for line in self.sh_bundle_lines:
                    product_line_vals = {
                        'picking_id': picking_id.id,
                        'location_id': src_location.id,
                        'location_dest_id': dest_location.id,
                        'name': line.sh_product_id.name,
                        'product_id': line.sh_product_id.id,
                        'product_uom': line.sh_bundle_uom.id,
                        'product_uom_qty': line.sh_bundle_quantity,
                        'state': 'draft',
                    }
                    product_lines.append((0, 0, product_line_vals))
                picking_id.move_ids_without_package = product_lines
        elif context.get('active_model') == 'purchase.order':
            purchase_order = self.env['purchase.order'].sudo().search(
                [('id', '=', context.get('active_id'))], limit=1)
            if purchase_order and self.sh_bundle_lines:
                product_lines = []
                line_vals = {}
                line_vals = {
                    'order_id': purchase_order.id,
                    'product_id': self.sh_bundle_id.product_variant_id.id,
                    'name': self.sh_bundle_id.product_variant_id.name,
                    'date_planned': fields.Datetime.now(),
                    'product_uom': self.sh_bundle_id.product_variant_id.uom_id.id,
                    'product_qty': self.sh_qty,
                    'price_unit': self.sh_bundle_id.list_price,
                }
                product_lines.append((0, 0, line_vals))
                for line in self.sh_bundle_lines:
                    product_line_vals = {
                        'order_id': purchase_order.id,
                        'product_id': line.sh_product_id.id,
                        'name': line.sh_product_id.name,
                        'date_planned': fields.Datetime.now(),
                        'product_uom': line.sh_bundle_uom.id,
                        'product_qty': line.sh_bundle_quantity,
                        'price_unit': 0.0,
                    }
                    product_lines.append((0, 0, product_line_vals))
                purchase_order.order_line = product_lines
        elif context.get('active_model') == 'account.move':
            account_invoice = self.env['account.move'].sudo().search(
                [('id', '=', context.get('active_id'))], limit=1)
            accounts = self.sh_bundle_id.get_product_accounts(
                account_invoice.fiscal_position_id)
            if account_invoice.move_type in ['out_invoice', 'out_refund'] and self.sh_bundle_lines:
                product_lines = []
                line_vals = {}
                line_vals = {
                    'move_id': account_invoice.id,
                    'account_id': accounts['income'].id,
                    'product_id': self.sh_bundle_id.product_variant_id.id,
                    'name': self.sh_bundle_id.product_variant_id.name,
                    'product_uom_id': self.sh_bundle_id.product_variant_id.uom_id.id,
                    'quantity': self.sh_qty,
                    'price_unit': self.sh_bundle_id.list_price,
                }
                product_lines.append((0, 0, line_vals))
                for line in self.sh_bundle_lines:
                    product_line_vals = {
                        'move_id': account_invoice.id,
                        'account_id': accounts['income'].id,
                        'product_id': line.sh_product_id.id,
                        'name': line.sh_product_id.name,
                        'product_uom_id': line.sh_bundle_uom.id,
                        'quantity': line.sh_bundle_quantity,
                        'price_unit': 0.0,
                    }
                    product_lines.append((0, 0, product_line_vals))
                account_invoice.invoice_line_ids = product_lines
            elif account_invoice.move_type in ['in_invoice', 'in_refund'] and self.sh_bundle_lines:
                product_lines = []
                line_vals = {}
                line_vals = {
                    'move_id': account_invoice.id,
                    'account_id': accounts['expense'].id,
                    'product_id': self.sh_bundle_id.product_variant_id.id,
                    'name': self.sh_bundle_id.product_variant_id.name,
                    'product_uom_id': self.sh_bundle_id.product_variant_id.uom_id.id,
                    'quantity': self.sh_qty,
                    'price_unit': self.sh_bundle_id.list_price,
                }
                product_lines.append((0, 0, line_vals))
                for line in self.sh_bundle_lines:
                    product_line_vals = {
                        'move_id': account_invoice.id,
                        'account_id': accounts['expense'].id,
                        'product_id': line.sh_product_id.id,
                        'name': line.sh_product_id.name,
                        'product_uom_id': line.sh_bundle_uom.id,
                        'quantity': line.sh_bundle_quantity,
                        'price_unit': 0.0,
                    }
                    product_lines.append((0, 0, product_line_vals))
                account_invoice.invoice_line_ids = product_lines


class ShProductBundleWizardLine(models.TransientModel):
    _name = 'sh.product.bundle.wizard.line'
    _description = 'Bundle Wizard Lines'

    wizard_id = fields.Many2one('sh.product.bundle.wizard', 'Wizard ID')
    sh_product_id = fields.Many2one(
        'product.product', 'Product', required=True)
    sh_bundle_quantity = fields.Float("Quantity")
    sh_bundle_uom = fields.Many2one("uom.uom", "Unit Of Measure")
