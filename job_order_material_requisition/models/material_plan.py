# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class MaterialPlanning(models.Model):
    _inherit = 'material.plan'
    
    
    requisition_line = fields.Many2one(
        'material.purchase.requisition.line',
        string='Requisition Line',
        readonly=True,
    )
    requisition_type = fields.Selection(
        selection=[
            ('internal','Internal Picking'),
            ('purchase','Purchase Order'),
        ],
        string='Requisition Action',
        default='internal',
        required=False,
    )