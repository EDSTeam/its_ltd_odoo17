# -*- coding: utf-8 -*-

from odoo import models, fields, api

PROJECT_TASK_READABLE_FIELDS = {
    'purchaseorder_line_ids',
    'subcontractor_id',
    'custom_contractor_partner_id',
    'is_subcontractor_joborder',
}

class ProjectTask(models.Model):
    _inherit = 'project.task'

    purchaseorder_line_ids = fields.One2many(
        'custom.contract.po.line',
        'sub_contractor_id',
        string='Material Plan',
    )
    subcontractor_id = fields.Many2one(
        'project.task',
        string='Subcontractor Joborder',
    )
    custom_contractor_partner_id = fields.Many2one(
        'res.partner',
        string='Subcontractor',
        readonly=True,
    )
    is_subcontractor_joborder = fields.Boolean(
        string='Subcontractor Job order',
        copy=False,
        default=False,
        readonly=True,
    )

    # @api.multi #odoo13
    def show_purchase_order(self):
        self.ensure_one()
        res = self.env.ref('purchase.purchase_rfq')
        res = res.sudo().read()[0]
        res['domain'] = str([('subcontractor_id', '=', self.id)])
        return res

    # @api.multi #odoo13
    def show_subcontractor_jobs(self):
        self.ensure_one()
        res = self.env.ref('job_order_subcontracting.action_subcontractor_job')
        res = res.sudo().read()[0]
        res['domain'] = str([
            ('parent_task_id', '=', self.id),
            ('is_subcontractor_joborder', '=', True),
        ])
        return res
    
    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS | PROJECT_TASK_READABLE_FIELDS

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
