# -*- coding: utf-8 -*-

from odoo import models, fields

class MaterialPlan(models.Model):
    _inherit = 'material.plan'
    
    custom_material_job_id = fields.Many2one(
        'job.cost.line',
        string='Job Cost Line',
        readonly=False,
    )
    custom_job_cost_id = fields.Many2one(
        'job.costing',
        string='Job Cost Sheet',
        related='custom_material_job_id.direct_id',
        store=True,
        readonly=False,
    )
    is_material_created = fields.Boolean(
        string='Is Created ?',
        readonly=True,
        copy=False,
    )
