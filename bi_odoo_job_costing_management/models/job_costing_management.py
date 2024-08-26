# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)
from odoo.tools import html2plaintext
from odoo.exceptions import UserError, ValidationError

class JobCostSheet(models.Model):
    _name = 'job.cost.sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Job Cost Sheet"
    _order = 'sequence desc'

    name = fields.Char(string="Name",required=True)
    sequence = fields.Char(string='Sequence', readonly=True,copy=False,default=lambda self: ('New'))
    project_id = fields.Many2one('project.project',string='Project')
    analytic_ids = fields.Many2one('account.analytic.account',string="Analytic Account")
    job_order_id = fields.Many2one('job.order','Job Order')
    job_issue_customer_id = fields.Many2one('res.partner','Job Issue Customer')
    create_date = fields.Datetime(string="Create Date",default=datetime.now())
    close_date = fields.Datetime(string="Close Date",default=datetime.now())
    create_by_id = fields.Many2one('res.users','Created By')
    material_job_cost_line_ids = fields.One2many('job.cost.line','material_job_cost_sheet_id','Material Job Cost Line')
    labour_job_cost_line_ids = fields.One2many('job.cost.line','labour_job_cost_sheet_id','Labout Job Cost Line')
    overhead_job_cost_line_ids = fields.One2many('job.cost.line','overhead_job_cost_sheet_id','Overhead Job Cost Line')
    total_material_cost = fields.Float(compute='_compute_total_material_cost',string="Total Material Cost",default=0.0)
    total_labour_cost = fields.Float(compute='_compute_total_labour_cost',string='Total Labour Cost',default=0.0)
    total_overhead_cost = fields.Float(compute='_compute_total_overhead_cost',string='Total Overhead Cost',default=0.0)
    total_cost = fields.Float(compute='_compute_total_cost',string='Total Cost',default=0.0)
    job_cost_description = fields.Text('Job Cost Description')
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")
    stage = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('approve','Approved'),('done','Done')],'Stage',copy=False,default='draft')
    purchase_order_line_count = fields.Integer('Purchase Order Line', compute='_get_purchase_order_line_count')
    invoice_line_count = fields.Integer('Invoice Order Line', compute='_get_invoice_line_count')
    purchase_id = fields.One2many('purchase.order.line', 'job_cost_sheet_id', string='Purchase Order')
    invoice_id = fields.One2many('account.move', 'job_cost_sheet_id')
    company_id = fields.Many2one('res.company',string="Company")
    sale_reference = fields.Text(string="Description Sale Reference")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['sequence'] = self.env['ir.sequence'].next_by_code('job.cost.sheet') or 'New'
            if vals.get('create_date') and vals.get('close_date'):
                if vals['create_date'] > vals['close_date']:
                    raise ValidationError(_('Close date is must be greater than Create date'))
        result = super(JobCostSheet, self).create(vals_list)
        return result

    def write(self,vals):
        if not self.sequence:
            vals['sequence'] = self.env['ir.sequence'].next_by_code('job.cost.sheet') or 'New'
        return super(JobCostSheet, self).write(vals)

    def requistion_line_button(self):
        self.ensure_one()
        return {
            'name': 'Material Requisition',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'material.purchase.requisition',
            'domain': [('id', '=', self.mapped('material_requisition_id').mapped('requisition_id').ids)],
        }
    def _get_purchase_order_line_count(self):
        count = 0.0
        for job_cost_sheet in self:
            purchase_order_line_ids = self.env['purchase.order.line'].search([('job_cost_sheet_id', '=', job_cost_sheet.id),('state','!=','draft')])
            purchase_ids = self.env['purchase.order'].search([('id', 'in', purchase_order_line_ids.order_id.ids)])
            job_cost_sheet.purchase_order_line_count = len(purchase_ids)

    def purchase_order_line_button(self):
        return {
            'name': 'Purchase Order',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('id', 'in', self.purchase_id.order_id.ids)],
        }

    def _get_invoice_line_count(self):
        for job_cost_sheet in self:
            invoice_line_ids = self.env['account.move.line'].search([('job_cost_sheet_id','=',job_cost_sheet.id),('move_id.state','!=','draft')])
            invoice_ids = self.env['account.move'].search([('job_cost_sheet_id','=',job_cost_sheet.id),('move_type','=','in_invoice')])
            job_cost_sheet.invoice_line_count = len(invoice_ids)

    def invoice_line_button(self):
        self.ensure_one()
        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('id', '=', self.invoice_id.ids)],
        }

    def action_confirm(self):
        if  self.create_date and self.close_date:
            if self.create_date > self.close_date:
                raise ValidationError(_('Close date is must be greater than Create date'))
        else:
            raise ValidationError(_('Please Enter Date'))
        confirm_stage = self.write({'stage':'confirm'})
        return confirm_stage

    def action_done(self):
        requisition_line_ids = self.env['material.purchase.requisition'].search([])
        if requisition_line_ids:
            for requisition_line in requisition_line_ids:
                if requisition_line.job_cost_sheet_id.id == self.id:
                    if requisition_line.state == 'new'\
                            or requisition_line.state == 'department_approval'\
                            or requisition_line.state == 'ir_approve':
                        raise ValidationError("Sorry !!! Please Approve Requisition First")
        done_stage = self.write({'stage':'done'})
        return done_stage

    def action_approve(self):
        approve_stage = self.write({'stage':'approve'})
        return approve_stage

    def action_create_purchase_requisition(self):
        self.ensure_one()
        context = dict(self.env.context or {})
        return {
            'name': 'Purchase Requisitions Details',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.requisitions.details',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'context': context,
            'target': 'new',
            }

    @api.onchange('project_id')
    def change_analytic_tags(self):
        for rec in self:
            if rec.project_id:
                rec.write({'analytic_ids':rec.project_id.analytic_account_id})

    @api.onchange('job_order_id')
    def update_material_labour_overhead(self):
        material_line = []
        labour_line = []
        overhead_line = []
        if self.job_order_id:
            for material in self.job_order_id.material_planning_ids:
                if material.job_type_id.job_type == "material":
                    material_ids = self.env['job.cost.line'].create({
                        'job_type_id' : material.job_type_id.id,
                        'product_id' : material.product_id.id,
                        'description' : material.description,
                        'quantity' : material.quantity,
                        'unit_price' : material.product_id.standard_price,
                        'uom_id' :material.uom_id.id,
                        })
                    material_line.append(material_ids.id)
                elif material.job_type_id.job_type == "labour":
                    labour_ids = self.env['job.cost.line'].create({
                        'job_type_id' : material.job_type_id.id,
                        'product_id' : material.product_id.id,
                        'description' : material.description,
                        'quantity' : material.quantity,
                        'hours' : material.quantity,
                        'unit_price' : material.product_id.standard_price,
                        'uom_id' :material.product_id.uom_id.id,
                        })
                    labour_line.append(labour_ids.id)
                elif material.job_type_id.job_type == "overhead":
                    overhead_ids = self.env['job.cost.line'].create({
                        'job_type_id' : material.job_type_id.id,
                        'product_id' : material.product_id.id,
                        'description' : material.description,
                        'unit_price' : material.product_id.standard_price,
                        'quantity' : material.quantity,
                        'uom_id' :material.uom_id.id,
                        })
                    overhead_line.append(overhead_ids.id)
            self.update({
                'project_id':self.job_order_id.project_id.id,
                'material_job_cost_line_ids':[(6 , 0 , material_line)],
                'labour_job_cost_line_ids' :[(6 , 0 , labour_line)],
                'overhead_job_cost_line_ids' :[(6 , 0 , overhead_line)],
                })

    def _compute_total_material_cost(self):
        total = 0.0
        for line in self.material_job_cost_line_ids:
            total += line.subtotal
        self.total_material_cost = total

    def _compute_total_labour_cost(self):
        total = 0.0
        for line in self.labour_job_cost_line_ids:
            total += line.subtotal
        self.total_labour_cost = total

    def _compute_total_overhead_cost(self):
        total = 0.0
        for line in self.overhead_job_cost_line_ids:
            total += line.subtotal
        self.total_overhead_cost = total

    def _compute_total_cost(self):
        total = 0.0
        for sheet in self:
            total = sheet.total_material_cost + sheet.total_labour_cost + sheet.total_overhead_cost
            sheet.total_cost = total

    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id.id

class JobCostLine(models.Model):
    _name = "job.cost.line"
    _description = "Job Cost Line"

    material_job_cost_sheet_id = fields.Many2one('job.cost.sheet','Material Job Cost Sheet')
    labour_job_cost_sheet_id = fields.Many2one('job.cost.sheet','Labour Job Cost Sheet')
    overhead_job_cost_sheet_id = fields.Many2one('job.cost.sheet','Overhead Job Cost Sheet')
    date = fields.Datetime('Date',default=datetime.now())
    job_type_id = fields.Many2one('job.type',string='Job Type')
    product_id = fields.Many2one('product.product','Product')
    description = fields.Text('Description')
    reference = fields.Char('Reference')
    quantity = fields.Float('Quantity',default=1.0)
    uom_id = fields.Many2one('uom.uom','Unit Of Measure')
    unit_price = fields.Float('Cost/Unit Price',default=0.0)
    actual_purchase_qty = fields.Float(compute='_compute_purchase_quantity',string='Actual Purchased Quantity',default=0.0)
    actual_invoice_qty = fields.Float(compute='_compute_invoice_quantity',string='Actual Invoice Quantity',default=0.0)
    subtotal = fields.Float(compute='onchange_quantity',string='Sub Total')
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")
    job_type = fields.Selection([('material','Material'),('labour','Labour'),('overhead','Overhead')],string="Job Cost Order Type")
    invoiced_qty = fields.Float("Invoiced Quantity", store=True)
    hours = fields.Float('Hours',default=0.0)
    actual_timesheet_hours = fields.Float('Actual Timesheet Hours',default=0.0)
    basis = fields.Char('Basis')

    def _compute_purchase_quantity(self):
        for line in self:
            qty = 0
            purchase_order_line_ids = self.env['purchase.order.line'].search([('product_id', '=', line.product_id.id),('state','!=','draft')])
            for purchase in purchase_order_line_ids:
                if line.product_id.id == purchase.product_id.id:
                    if purchase.job_cost_sheet_id.id in [line.material_job_cost_sheet_id.id , line.overhead_job_cost_sheet_id.id]:
                        if purchase.job_cost_sheet_id.id != False:
                            qty += purchase.product_qty
            line.actual_purchase_qty = qty


    def _compute_invoice_quantity(self):
        for line in self:
            qty = 0
            invoice_line_ids = self.env['account.move.line'].search([('product_id', '=', line.product_id.id),('move_id.state','!=','draft'),('move_id.move_type','=','in_invoice')])
            for invoice in invoice_line_ids:
                if line.product_id.id == invoice.product_id.id:
                    if invoice.job_cost_sheet_id.id in [line.material_job_cost_sheet_id.id , line.overhead_job_cost_sheet_id.id]:
                        if invoice.job_cost_sheet_id.id != False:
                            qty += invoice.quantity
            line.actual_invoice_qty = qty

    @api.onchange('quantity', 'unit_price')
    def onchange_quantity(self):
        for line in self:
            price = line.quantity * line.unit_price
            if line.hours:
                line.hours = line.quantity
                price = line.hours * line.unit_price
            line.subtotal = price

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = {}
        if not self.product_id:
            return res
        self.unit_price = self.product_id.standard_price
        self.uom_id = self.product_id.uom_id.id
        self.description = self.product_id.name

    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id

class JobOrder(models.Model):
    _name = 'job.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Job Order"


    name = fields.Char(string="Name",required=True)
    project_id = fields.Many2one('project.project',string='Project')
    user_id = fields.Many2one('res.users',string='Assigned To')
    planned_hours = fields.Float(string="Initially Planned Hours")
    start_date = fields.Datetime(string="Starting Date",default=datetime.now())
    end_date = fields.Datetime(string="Ending Date")
    deadline_date = fields.Datetime(string="Deadline")
    tag_ids = fields.Many2many('project.tags',string="Tags")
    description = fields.Html(string="Description")
    timesheet_ids = fields.One2many('account.analytic.line','account_analytic_line_id',string="Timesheet")
    material_planning_ids = fields.One2many('material.planning','material_id',string="Product Material Planning")
    consumed_material_ids = fields.One2many('material.planning','consumed_material_id',string="Consumed Material")
    material_requisitions_ids = fields.One2many('material.purchase.requisition','job_order_id',string="Material Requisitions")
    stock_move_ids = fields.One2many('stock.move','stock_move_id',string=" Stock Move")
    priority = fields.Selection([('0','Low'), ('1','Normal'), ('2','High')], 'Priority')
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")
    active = fields.Boolean(default=True)
    job_cost_count = fields.Integer('Job Cost', compute='_get_job_cost_count')
    stock_move_count = fields.Integer('Stock Move', compute='_get_stock_move_count')
    job_note_count = fields.Integer('Job Note', compute='_get_job_note_count')

    def _get_job_note_count(self):
        for job_order in self:
            job_note_ids = self.env['job.note'].search([('job_order_id','=',job_order.id)])
            job_order.job_note_count = len(job_note_ids)

    def job_note_button(self):
        self.ensure_one()
        return {
            'name': 'Job Note',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'job.note',
            'domain': [('job_order_id', '=', self.id)],
        }


    def _get_job_cost_count(self):
        for job_order in self:
            job_cost_ids = self.env['job.cost.sheet'].search([('project_id','=',job_order.id)])
            job_order.job_cost_count = len(job_cost_ids)


    def project_job_cost_button(self):
        self.ensure_one()
        return {
            'name': 'Job Cost Sheet',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'job.cost.sheet',
            'domain': [('job_order_id', '=', self.id)],
        }

    def _get_stock_move_count(self):
        for job_order in self:
            stock_move_ids = self.env['stock.move'].search([('stock_move_id','=',job_order.id)])
            job_order.stock_move_count = len(stock_move_ids)

    def stock_move_button(self):
        self.ensure_one()
        return {
            'name': 'Stock Move',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'stock.move',
            'domain': [('stock_move_id', '=', self.id)],
        }

    @api.model_create_multi
    def create(self, vals_list):
        result = super(JobOrder, self).create(vals_list)
        for vals in vals_list:
            product_id =""
            if product_id in vals:
                stock_picking_ids = self.env['stock.picking'].search([('construction_project_id','=',vals['project_id'])])
                for picking in stock_picking_ids:
                    for move in picking.move_ids_without_package:
                        move.write({'stock_move_id':result.id})
                    picking.write({'material_requisition_id':result.id})
            if 'timesheet_ids' in vals:
                for time in vals['timesheet_ids']:
                    if 'task_id' in time:
                        task_id = self.env['project.task'].browse(time['task_id'])
                        task_id.update({
                            'employee_id': time['employee_id'],
                            'name' : time['name'],
                            'task_id' : time['task_id'],
                            'unit_amount' : time['unit_amount']
                            })
        return result

    def write(self,vals):
        res = super(JobOrder, self).write(vals)
        if self.project_id:
            stock_picking_ids = self.env['stock.picking'].search([('construction_project_id','=',self.project_id.id)])
            for picking in stock_picking_ids:
                for move in picking.move_ids_without_package:
                    move.write({'stock_move_id':self.id})
                picking.write({'material_requisition_id':self.id})
        if 'timesheet_ids' in vals:
            for time in vals['timesheet_ids']:
                if 'task_id' in time:
                    task_id = self.env['project.task'].browse(time['task_id'])
                    task_id.update({
                        'employee_id': time['employee_id'],
                        'name' : time['name'],
                        'task_id' : time['task_id'],
                        'unit_amount' : time['unit_amount']
                        })
        return res

    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id.id

class MaterialPlanning(models.Model):
    _name = "material.planning"
    _description = "Material Planning"

    @api.onchange('job_type_id')
    def _return_domain(self):
        if self.job_type_id:
            if self.job_type_id.job_type == "labour":
                 return {'domain': {'product_id': [("type", '=', "service")]}}
        return {'domain': {'product_id': []}}

    job_type_id = fields.Many2one('job.type' , string = "Job Type")
    material_id = fields.Many2one('job.order','Job Material Planning')
    consumed_material_id = fields.Many2one('job.order','Job Consumed Material')
    product_id = fields.Many2one('product.product','Product' )
    description = fields.Text('Description')
    quantity = fields.Float('Quantity',default=1.0)
    uom_id = fields.Many2one('uom.uom','Unit Of Measure')
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")
    product_type = fields.Selection([('material_planning','Material Planning'),('consumed_material','Consumed Material')],string="Product Type")

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = {}
        if not self.product_id:
            return res
        self.uom_id = self.product_id.uom_id.id
        self.description = self.product_id.name

    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id

class StockMove(models.Model):
    _inherit = "stock.move"

    stock_move_id = fields.Many2one('job.order','Job Order', related = "picking_id.material_requisition_id")
    name = fields.Char('Name')

class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    account_analytic_line_id = fields.Many2one('job.order','Job Timesheet')

class ProjectProject(models.Model):
    _inherit = 'project.project'

    def _get_job_cost_count(self):
        for project in self:
            job_cost_ids = self.env['job.cost.sheet'].search([('project_id','=',project.id)])
            project.job_cost_count = len(job_cost_ids)

    def project_job_cost_button(self):
        self.ensure_one()
        return {
            'name': 'Job Cost Sheet',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'job.cost.sheet',
            'domain': [('project_id', '=', self.id)],
        }

    job_cost_sheet_id = fields.Many2one('job.cost.sheet','Responsible Person')
    job_cost_count  =  fields.Integer('Job Cost', compute='_get_job_cost_count')


class JobNote(models.Model):
    _name = 'job.note'
    _description = "Job Note"
    _order = 'sequence desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        return self.env['project.task.type'].search([('user_id', '=', self.env.uid)], limit=1)

    tag_ids = fields.Many2many('project.tags','tag_id',string="Tag")
    memo = fields.Html(string="Body")
    job_order_id = fields.Many2one('job.order','Job Order')
    responsible_user = fields.Many2one('res.users','Responsible Person')
    job_note_id = fields.Many2one('job.order',' Job Order')
    name = fields.Text(compute='_compute_name', string='Note Summary', store=True)
    user_id = fields.Many2one('res.users', string='Owner', default=lambda self: self.env.uid)
    sequence = fields.Integer('Sequence')
    stage_id = fields.Many2one('project.task.type', compute='_compute_stage_id',
        inverse='_inverse_stage_id', string='Stage')
    stage_ids = fields.Many2many('project.task.type',
        string='Stages of Users',  default=_get_default_stage_id)
    open = fields.Boolean(string='Active', default=True)
    date_done = fields.Date('Date done')
    color = fields.Integer(string='Color Index')

    @api.depends('memo')
    def _compute_name(self):
        """ Read the first line of the memo to determine the note name """
        for note in self:
            text = html2plaintext(note.memo) if note.memo else ''
            note.name = text.strip().replace('*', '').split("\n")[0]


    def _compute_stage_id(self):
        for note in self:
            for stage in note.stage_ids.filtered(lambda stage: stage.user_id == self.env.user):
                note.stage_id = stage

    def _inverse_stage_id(self):
        for note in self.filtered('stage_id'):
            note.stage_ids = note.stage_id + note.stage_ids.filtered(lambda stage: stage.user_id != self.env.user)

    @api.model
    def name_create(self, name):
        return self.create({'memo': name}).name_get()[0]

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if groupby and groupby[0] == "stage_id":
            stages = self.env['project.task.type'].search([('user_id', '=', self.env.uid)])
            if stages:
                result = [{
                    '__context': {'group_by': groupby[1:]},
                    '__domain': domain + [('stage_ids', 'in', stage.id)],
                    'stage_id': (stage.id, stage.name),
                    'stage_id_count': self.search_count(domain + [('stage_ids', '=', stage.id)]),
                    '__fold': stage.fold,
                } for stage in stages]
                nb_notes_ws = self.search_count(domain + [('stage_ids', 'not in', stages.ids)])
                if nb_notes_ws:
                    dom_not_in = ('stage_ids', 'not in', stages.ids)
                    if result and result[0]['stage_id'][0] == stages[0].id:
                        dom_in = result[0]['__domain'].pop()
                        result[0]['__domain'] = domain + ['|', dom_in, dom_not_in]
                        result[0]['stage_id_count'] += nb_notes_ws
                    else:
                        result = [{
                            '__context': {'group_by': groupby[1:]},
                            '__domain': domain + [dom_not_in],
                            'stage_id': (stages[0].id, stages[0].name),
                            'stage_id_count': nb_notes_ws,
                            '__fold': stages[0].name,
                        }] + result
            else:
                nb_notes_ws = self.search_count(domain)
                if nb_notes_ws:
                    result = [{
                        '__context': {'group_by': groupby[1:]},
                        '__domain': domain,
                        'stage_id': False,
                        'stage_id_count': nb_notes_ws
                    }]
                else:
                    result = []
            return result
        return super(JobNote, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)


    def action_close(self):
        return self.write({'open': False, 'date_done': fields.date.today()})

    def action_open(self):
        return self.write({'open': True})


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    boq_type = fields.Selection([('machine_qui','Machinery / Equipment'),('worker','Worker / Resource'),('work_package','Work Cost Package'),('subcontract','Subcontract')],'BOQ Type')

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    material_requisition_id = fields.Many2one('job.order','Job Order')
    job_order_user_id = fields.Many2one('res.users',string="Task / Job Order User")
    construction_project_id = fields.Many2one('project.project',string="Construction Project")
    analytic_account_id = fields.Many2one('account.analytic.account',string="Analytic Account")

class JobType(models.Model):
    _name = 'job.type'
    _description = "Job Type"

    name = fields.Char("Name")
    code = fields.Char("Code")
    job_type = fields.Selection([('material','Material'),('labour','Labour'),('overhead','Overhead')],"Job Type")

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    job_order_id = fields.Many2one('job.order',string="Job Cost Center")
    job_cost_sheet_id = fields.Many2one('job.cost.sheet',string="Job Cost Sheet" , related = "order_id.job_id")
    project_id = fields.Many2one('project.project', string='Project')

    def _prepare_account_move_line(self):
        res = super(PurchaseOrderLine , self)._prepare_account_move_line()
        res.update({
            'job_cost_sheet_id' : self.job_cost_sheet_id.id
        })
        return res


class InvoiceLine(models.Model):
    _inherit = 'account.move.line'

    job_cost_sheet_id = fields.Many2one('job.cost.sheet',string="Job Cost Center" , related = "move_id.job_cost_sheet_id")

class accountmoveinherited(models.Model):
    _inherit = 'account.move'

    job_cost_sheet_id = fields.Many2one('job.cost.sheet',string="Job Cost Center")

    @api.model
    def write(self, vals):
        job_id = self.line_ids.mapped('purchase_order_id').job_id
        if job_id:
            vals.update({'job_cost_sheet_id': job_id.id})
        result = super(accountmoveinherited, self).write(vals)
        return result


    @api.onchange('purchase_vendor_bill_id', 'purchase_id')
    def _onchange_purchase_auto_complete(self):
        if self.purchase_vendor_bill_id.vendor_bill_id:
            self.invoice_vendor_bill_id = self.purchase_vendor_bill_id.vendor_bill_id
            self._onchange_invoice_vendor_bill()
        elif self.purchase_vendor_bill_id.purchase_order_id:
            self.purchase_id = self.purchase_vendor_bill_id.purchase_order_id
        self.purchase_vendor_bill_id = False

        if not self.purchase_id:
            return
        self.partner_id = self.purchase_id.partner_id
        self.fiscal_position_id = self.purchase_id.fiscal_position_id
        self.invoice_payment_term_id = self.purchase_id.payment_term_id
        self.currency_id = self.purchase_id.currency_id
        self.job_cost_sheet_id = self.purchase_id.job_id
        po_lines = self.purchase_id.order_line - self.line_ids.mapped('purchase_line_id')
        for line in po_lines.filtered(lambda l: not l.display_type):
            self.invoice_line_ids += self.env['account.move.line'].new(
                line._prepare_account_move_line(self)
            )
        origins = set(self.line_ids.mapped('purchase_line_id.order_id.name'))
        self.invoice_origin = ','.join(list(origins))
        refs = set(self.line_ids.mapped('purchase_line_id.order_id.partner_ref'))
        refs = [ref for ref in refs if ref]
        self.ref = ','.join(refs)
        if len(refs) == 1:
            self._invoice_payment_ref = refs[0]

        self.purchase_id = False




    def assigned_invoiced_qty(self, job_cost_sheet):
        job_cost_sheet_obj = self.env['job.cost.sheet'].sudo().browse(job_cost_sheet)
        for am_lines in self.invoice_line_ids:
            for lines in job_cost_sheet_obj.material_job_cost_line_ids:
                if lines.product_id.id == am_lines.product_id.id:
                    lines.invoiced_qty += float(am_lines.quantity)
            for lines in job_cost_sheet_obj.labour_job_cost_line_ids:
                if lines.product_id.id == am_lines.product_id.id:
                    lines.invoiced_qty += float(am_lines.quantity)
            for lines in job_cost_sheet_obj.overhead_job_cost_line_ids:
                if lines.product_id.id == am_lines.product_id.id:
                    lines.invoiced_qty += float(am_lines.quantity)





    def action_post(self):
        if self.job_cost_sheet_id.id:
            self.assigned_invoiced_qty(self.job_cost_sheet_id.id)
        return super(accountmoveinherited, self).action_post()


class PruchaseOrder(models.Model):
    _inherit = 'purchase.order'

    job_id = fields.Many2one('job.cost.sheet',string='Job Cost Sheet')
    project_id = fields.Many2one('project.project',string='Project')

