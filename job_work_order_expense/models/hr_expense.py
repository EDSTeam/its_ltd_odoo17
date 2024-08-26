# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class HrExpense(models.Model):
    _inherit="hr.expense"

    expense_project_id = fields.Many2one(
        'project.project',
        string='Project',
    )
    expense_task_id = fields.Many2one(
        'project.task',
        string='Job Order',
    )
    expense_img1 = fields.Binary(
        string="Photo 1",
    )
    expense_img2 = fields.Binary(
        string="Photo 2",
    )
    expense_img3 = fields.Binary(
        string="Photo 3",
    )
    expense_img4 = fields.Binary(
        string="Photo 4",
    )
    expense_img5 = fields.Binary(
        string="Photo 5",
    )

    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
