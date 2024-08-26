# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SubContractor(models.TransientModel):
    _name = 'sub.contractor'
    _description = 'Sub Contractor Job'

    user_id = fields.Many2one(
        'res.users',
        string='Responsible User/ Subcontractor User',
        required=True,
    )
    description = fields.Text(
        string='Job Description',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Subcontractor',
        required=True,
    )
    name = fields.Char(
        string='Job',
        required=True,
    )

    # @api.multi #odoo13
    def set_subcontractor_job(self):
        self.ensure_one()
        task_id = self._context.get('active_id', False)
        task = self.env['project.task'].browse(task_id)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        joborder_vals = {
            'name': self.name,
            'project_id': task.project_id.id,
            # 'display_project_id': task.project_id.id,
            'job_number': task.job_number,
            # 'user_id': self.user_id.id,
            # 'activity_user_id': self.user_id.id,
            'user_ids': self.user_id.ids,
            'description': self.description,
            'parent_task_id': task_id,
            'parent_id': task_id,#ODOO 13 
            'partner_id': self.partner_id.id,
            'custom_contractor_partner_id': self.partner_id.id,
            'is_subcontractor_joborder': True,
        }
        joborder = self.env['project.task'].create(joborder_vals)
        if joborder.project_id:
            joborder.project_id.message_subscribe([self.partner_id.id])

        ctx = self._context.copy()
        url = base_url + '/my/subcontractor/' + str(joborder.id)
        ctx.update({
            'url': url,
        })

        if self.partner_id:
            template = self.env.ref('job_order_subcontracting.email_subcontractor_template')
            template.with_context(ctx).send_mail(joborder.id)

        # res = self.env.ref('odoo_job_costing_management.action_view_job_orders')
        # res = res.sudo().read()[0]
        res = self.env['ir.actions.act_window']._for_xml_id('odoo_job_costing_management.action_view_job_orders')
        res['domain'] = str([('id', '=', joborder.id)])
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
