# -*- coding: utf-8 -*-
# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
#from ast import literal_eval


class projectTask(models.Model):
    _inherit = 'project.task'
    

    stock_move_id = fields.One2many(
        'stock.move',
        'task_id',
        string = 'Move Ids',
        readonly = True,
    )

    #@api.multi
    def view_stock_moves(self):
         for rec in self:
            stock_move_list = []
            for move in rec.move_ids:
                # stock_move_list += move.requisition_id.delivery_picking_id.move_lines.ids
                # stock_move_list += move.requisition_id.delivery_picking_id.move_line_ids.ids
                stock_move_list += move.move_line_ids.ids
            # result = self.env.ref('stock.stock_move_action')
            # action_ref = result or False
            # result = action_ref.sudo().read()[0]
            result = self.env['ir.actions.act_window']._for_xml_id('stock.stock_move_action')
            result['context'] = {}
            result['domain'] = str(['|',('id', 'in', stock_move_list),('id', '=', self.stock_move_id.ids)])
            return result
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
