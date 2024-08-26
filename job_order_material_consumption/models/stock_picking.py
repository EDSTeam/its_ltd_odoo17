# -*- coding: utf-8 -*-
# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class Picking(models.Model):
    _inherit = 'stock.picking'

    project_id = fields.Many2one(
        'project.project',
        string='Project',
        copy=False,
    )
    
    task_id = fields.Many2one(
        'project.task', 
        string ='Job Order', 
        copy=False
    )
    
class StockMove(models.Model):
    _inherit = "stock.move"
    
    cust_project_id = fields.Many2one(
        'project.project',
        string='Project',
        related='picking_id.project_id',
    )

    task_id = fields.Many2one(
        'project.task', 
        string ='Job Order', 
        copy=False
    )
    
    consumption_type_id = fields.Many2one(
        'consumption.type', 
        string ='Consumption Type', 
        copy=False
    )
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
