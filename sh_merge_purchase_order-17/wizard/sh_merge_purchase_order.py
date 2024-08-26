# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


class MergePurchaseWizardLine(models.TransientModel):
    _name = 'sh.merge.purchase.wizard.line'
    _description = 'Merge Purchase Wizard Line'

    merge_line_id = fields.Many2one(
        'sh.mpo.merge.purchase.order.wizard', string='Merge Purchase Wizard Line')
    qty = fields.Float(string='Quantity')
    product_id = fields.Many2one(
        'product.product', string='Product')
    purchase_order_line_id = fields.Many2one(
        "purchase.order.line", string="Purchase Order Line")
    purchase_order_id = fields.Many2one(
        "purchase.order", string="Purchase Order")
    product_qty_available = fields.Float('Quantity On Hand')


class ShMpoMergePurchaseOrderWizard(models.TransientModel):
    _name = "sh.mpo.merge.purchase.order.wizard"
    _description = "Merge Purchase Order Wizard"

    partner_id = fields.Many2one("res.partner", string="Vendor", required=True)
    purchase_order_id = fields.Many2one(
        "purchase.order", string="Purchase Order")
    purchase_order_ids = fields.Many2many(
        "purchase.order", string="Purchase Orders")
    merge_type = fields.Selection([
        ("nothing", "Do Nothing"),
        ("cancel", "Cancel Other Purchase Orders"),
        ("remove", "Remove Other Purchase Orders"),
    ], default="nothing", string="Merge Type")

    merge_line_ids = fields.One2many(
        'sh.merge.purchase.wizard.line', 'merge_line_id', string='Merge RFQ Wizard')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    sh_is_merge_chatter_po = fields.Boolean(
        string=" Is Merged Chatter Message", default=True)

    sh_is_qty_available_po = fields.Boolean(
        string=" Is Qty available", default=False)

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        if self:
            self.purchase_order_id = False

    def action_merge_purchase_order(self):
        order_list = []
        purchase_order = False
        if self and self.partner_id and self.purchase_order_ids:
            if self.purchase_order_id:
                purchase_order = self.purchase_order_id
                order_list.append(self.purchase_order_id.id)
                order_line_vals = {"order_id": self.purchase_order_id.id}
                sequence = 10
                if self.purchase_order_id.order_line:
                    for existing_line in self.purchase_order_id.order_line:
                        existing_line.sudo().write({
                            'sequence': sequence
                        })
                        sequence += 1
                orders = self.env['purchase.order'].sudo().search(
                    [('id', '!=', self.purchase_order_id.id), ('id', 'in', self.purchase_order_ids.ids)], order='id asc')
                for order in orders:
                    if order.order_line:
                        for line in order.order_line:
                            for merge in self.merge_line_ids:
                                if merge.purchase_order_line_id.id == line.id:
                                    if self.company_id.sh_po_sub_merge_qty:
                                        if merge.qty <= line.product_qty:

                                            order_line_vals['product_qty'] = merge.qty
                                            SO = line.product_qty - merge.qty

                                            if SO > 0:
                                                line.product_qty = SO
                                            else:
                                                merged_line = line.copy(
                                                    default=order_line_vals)
                                                merged_line.sudo().write({
                                                    'sequence': sequence
                                                })
                                                sequence += 1
                                                line.unlink()
                                        else:
                                            raise UserError(
                                                _("%s Quantity is can't be more than Purchase Order (%s) Lines Quantity (%s)") % (merge.product_id.name, merge.purchase_order_id.name, line.product_qty))
                                    else:
                                        if merge.qty > line.product_qty:
                                            raise UserError(
                                                _("%s Quantity is can't be more than Purchase Order (%s) Lines Quantity (%s)") % (merge.product_id.name, merge.purchase_order_id.name, line.product_qty))
                                        else:
                                            order_line_vals['product_qty'] = merge.qty

                            if line.exists():
                                merged_line = line.copy(
                                    default=order_line_vals)
                                merged_line.sudo().write({
                                    'sequence': sequence
                                })
                                sequence += 1

                    # finally cancel or remove order
                    if self.merge_type == "cancel":
                        order.sudo().button_cancel()
                        order_list.append(order.id)
                    elif self.merge_type == "remove":
                        order.sudo().button_cancel()
                        order.sudo().unlink()

            else:
                created_po = self.env["purchase.order"].with_context({
                    "trigger_onchange": True,
                    "onchange_fields_to_trigger": [self.partner_id.id]
                }).create({"partner_id": self.partner_id.id,
                           "date_planned": datetime.now(),
                           })
                if created_po:
                    purchase_order = created_po
                    order_list.append(created_po.id)
                    order_line_vals = {"order_id": created_po.id}
                    sequence = 10
                    orders = self.env['purchase.order'].sudo().search(
                        [('id', 'in', self.purchase_order_ids.ids)], order='id asc')
                    for order in orders:
                        if order.order_line:
                            for line in order.order_line:
                                for merge in self.merge_line_ids:
                                    if merge.purchase_order_line_id.id == line.id:
                                        if self.company_id.sh_po_sub_merge_qty:
                                            if merge.qty <= line.product_qty:

                                                order_line_vals['product_qty'] = merge.qty
                                                SO = line.product_qty - merge.qty

                                                if SO > 0:
                                                    line.product_qty = SO
                                                else:
                                                    merged_line = line.copy(
                                                        default=order_line_vals)
                                                    merged_line.sudo().write({
                                                        'sequence': sequence
                                                    })
                                                    sequence += 1
                                                    line.unlink()
                                            else:
                                                raise UserError(
                                                    _("%s Quantity is can't be more than Purchase Order (%s) Lines Quantity (%s)") % (merge.product_id.name, merge.purchase_order_id.name, line.product_qty))
                                        else:
                                            if merge.qty > line.product_qty:
                                                raise UserError(
                                                    _("%s Quantity is can't be more than Purchase Order (%s) Lines Quantity (%s)") % (merge.product_id.name, merge.purchase_order_id.name, line.product_qty))
                                            else:
                                                order_line_vals['product_qty'] = merge.qty

                                if line.exists():
                                    merged_line = line.copy(
                                        default=order_line_vals)
                                    merged_line.sudo().write({
                                        'sequence': sequence
                                    })
                                    sequence += 1

                        # finally cancel or remove order
                        if self.merge_type == "cancel":
                            order.sudo().button_cancel()
                            order_list.append(order.id)
                        elif self.merge_type == "remove":
                            order.sudo().button_cancel()
                            order.sudo().unlink()

            # For Merge Chatter Message
            if purchase_order and self.sh_is_merge_chatter_po:
                self.env['sh.select.model.record.wizard'].sh_merge_chatter_message(
                    record=purchase_order)

            if order_list:
                return {
                    "name": _("Requests for Quotation"),
                    "domain": [("id", "in", order_list)],
                    "view_type": "form",
                    "view_mode": "tree,form",
                    "res_model": "purchase.order",
                    "view_id": False,
                    "type": "ir.actions.act_window",
                }

    @api.model
    def default_get(self, fields):
        res = super(ShMpoMergePurchaseOrderWizard, self).default_get(fields)
        active_ids = self._context.get("active_ids")
        line_list = []

        # Check for selected invoices ids
        if not active_ids:
            raise UserError(
                _("Programming error: wizard action executed without active_ids in context."))

        # Check if only one purchase order selected.
        if len(self._context.get("active_ids", [])) < 2:
            raise UserError(
                _("Please Select atleast two Requests for Quotation to perform merge operation."))

        purchase_orders = self.env["purchase.order"].browse(active_ids)

        # Check all purchase order are draft state
        if any(order.state not in ["draft", "sent"] for order in purchase_orders):
            raise UserError(
                _("You can only merge purchase orders which are in RFQ and RFQ Sent state"))

        # check stock dependency
        stock_app = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'stock')], limit=1)
        if stock_app.state != 'installed':
            sh_is_qty_available_po = False
        else:
            sh_is_qty_available_po = True

        for rec in purchase_orders:
            if rec.order_line:
                lines = rec.mapped('order_line')
                if lines:
                    for line in lines:
                        line_vals = {
                            'product_id': line.product_id.id,
                            'qty': line.product_qty,
                            'purchase_order_id': rec.id,
                            'purchase_order_line_id': line.id,
                            'product_qty_available': line.product_id.qty_available if sh_is_qty_available_po else None,
                        }
                        line_list.append((0, 0, line_vals))

        # return first purchase order partner id and purchase order ids,
        res.update({
            "partner_id": purchase_orders[0].partner_id.id if purchase_orders[0].partner_id else False,
            "purchase_order_ids": [(6, 0, purchase_orders.ids)],
            "merge_line_ids": line_list,
            'sh_is_qty_available_po': sh_is_qty_available_po or False,

        })
        return res
