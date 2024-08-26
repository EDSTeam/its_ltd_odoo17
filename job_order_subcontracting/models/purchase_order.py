# -*- coding: utf-8 -*-

from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    subcontractor_id = fields.Many2one(
        'project.task',
        string='Sub Contractor Job',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
