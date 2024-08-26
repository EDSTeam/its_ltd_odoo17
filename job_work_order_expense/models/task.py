# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit="project.task"

    # @api.multi
    def action_expense_view(self):
        for rec in self:
            expense_ids = self.env['hr.expense'].search([('expense_task_id', '=', rec.id)])
            # action = self.env.ref('hr_expense.hr_expense_actions_my_unsubmitted').sudo().read()[0]
            action = self.env['ir.actions.act_window']._for_xml_id('hr_expense.hr_expense_actions_my_all')
            action['domain'] = [('id', 'in', expense_ids.ids)]
            return action
            
    # @api.multi
    def action_expense_sheets_view(self):
        expense_sheet_obj = self.env['hr.expense.sheet']
        for rec in self:
            expense_ids = self.env['hr.expense'].search([('expense_task_id', '=', rec.id)])
            expense_sheet_ids = self.env['hr.expense.sheet'].search([('expense_line_ids', 'in', expense_ids.ids)])
            #action = self.env.ref('hr_expense.action_hr_expense_sheet_my_all').sudo().read()[0]
            action = self.env['ir.actions.act_window']._for_xml_id('hr_expense.action_hr_expense_sheet_my_all')
            action['domain'] = [('id', 'in', expense_sheet_ids.ids)]
            return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
