# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MaterialRequisition(models.TransientModel):
    _name = "material.purchase.requisition.wizard"
    _description = 'Material Requisition Wizard'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
        required=True,
    )
    operation_type = fields.Selection([
        ('exist', 'Existing Requisition'),
        ('create', 'Create a new Requisition'),
       
    ], 'Operation Type', required=True)

    material_requisition = fields.Many2one(
        'material.purchase.requisition',
        string='Material Requisition'
    )

   
    # @api.multi
    def action_create_reservation(self):
        self.ensure_one()
        # context = dict(self._context or {})
        # active_model = context.get('active_model')
        # active_ids = context.get('active_ids')
        # job_order = self.env[active_model].browse(active_ids)
        # vals = []
        
        # active_id = self._context.get('active_id')
        job_order = self.env['project.task'].browse(self._context.get('active_id'))
        custome_reservtion_obj = self.env['material.purchase.requisition']
        requisition_lines = self.env['material.purchase.requisition.line']
        material_requisition = self.material_requisition
        if self.operation_type == 'create':
            vals = {
                'request_date': fields.Datetime.now(),
                # 'task_user_id': job_order.user_id.id,
                'task_user_id': job_order.user_ids[0].id,
                'task_id':job_order.id,
                'employee_id': self.employee_id.id,
                'project_id':job_order.project_id.id,
                'department_id': self.employee_id.department_id.id,
            }
            reserv_move_id = custome_reservtion_obj.create(vals)
            material_requisition = reserv_move_id
            for line in job_order.material_plan_ids:
                if not line.requisition_line:
                    line_vals =  {
                        'product_id': line.product_id.id,
                        'description':line.description,
                        'qty': line.product_uom_qty,
                        'uom': line.product_uom.id,
                        'requisition_type':line.requisition_type,
                        'requisition_id':reserv_move_id.id,
                    }
                    purchase_requisition_line = requisition_lines.create(line_vals)
                    line.requisition_line = purchase_requisition_line
            
        if self.operation_type == 'exist':
            vals = {}
            for line in job_order.material_plan_ids:
                if not line.requisition_line:
                    line_vals =  {
                        'product_id': line.product_id.id,
                        'description':line.description,
                        'qty': line.product_uom_qty,
                        'uom': line.product_uom.id,
                        'requisition_type':line.requisition_type,
                        'requisition_id':self.material_requisition.id,
                    }
                    purchase_requisition_line = requisition_lines.create(line_vals)
                    line.requisition_line = purchase_requisition_line
            exit_reserv_move_id = custome_reservtion_obj.write(vals)
        # action = self.env.ref('material_purchase_requisitions.action_material_purchase_requisition').sudo().read()[0]
        action = self.env["ir.actions.actions"]._for_xml_id("material_purchase_requisitions.action_material_purchase_requisition")
        action['domain'] = [('id','=',material_requisition.id)]
        return action







            

        


