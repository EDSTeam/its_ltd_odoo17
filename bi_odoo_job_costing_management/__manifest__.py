# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Project Job Costing and Job Cost Sheet With Material Request Odoo',
    'version': '17.0.0.0',
    'category': 'Projects',
    'summary': """Apps Construction Job Costing construction Cost Sheet job contracting system Construction job order Material Planning On Job Order Construction Material request purchase Material request construction Vendor Contractors Labour estimation Construction Budget""",
    'description': """
        Project Job Costing and Job Cost Sheet.
        This modules helps to manage contracting,Job Costing and Job Cost Sheet inculding dynamic material request
    ODOO Project Contracting Project costing project calculation project cost calculation constuction project costing 
    odoo project cost sheet construction material request odoo construction project management construction billing system construction cost calculation
    Odoo calculate  cost of construction project job contract job contracting Construction job contracting job contract estimation cost estimation project estimation 
    odoo modules helps to manage contracting Job Costing and Job Cost Sheet inculding dynamic material request
    Odoo job costing bundle job costing in construction project cost Estimation construction cost Estimation in Odoo 
    Odoo Send Estimation to your Customers for materials labour overheads details in job estimation.
    Odoo Estimation for Jobs - Material Labour Overheads Material Esitmation
    Odoo Job estimation labour estimation Overheads estimation
        BrowseInfo developed a new odoo/OpenERP module apps.
        This module use for odoo Real Estate Management Construction management Building Construction
    Odoo Material Line on JoB Estimation Labour Lines on Job Estimation Overhead Lines on Job Estimation.
    Odoo create Quotation from the Job Estimation overhead on job estimation Construction Projects
    Odoo Budgets Notes Materials Material Request For Job Orders Add Materials
    Odoo Job Orders Create Job Orders Job Order Related Notes Issues Related Project
    Odoo Vendors project construction Vendors Contractors
    Odoo Construction Management Construction Activity Construction Jobs
    Odoo Job Order Construction Job Orders Issues Job Order Notes
    Odoo Construction Notes Job Order Reports
    Odoo Construction Reports Job Order Note Construction app
    odoo Project Report Task Report
    Odoo Construction Project - Project Manager real estate property
    Odoo propery management bill of material
    Odoo Material Planning On Job Order Bill of Quantity On Job Order
    Odoo Bill of Quantity construction Project job costing on manufacturing
    BrowseInfo developed a new odoo/OpenERP module apps.
    Material request is an instruction to procure a certain quantity of 
    Odoo materials by purchase internal transfer or manufacturing.So that goods are available when it require.
    Odoo Material request for purchase, internal transfer or manufacturing
    Odoo Material request for internal transfer Material request for purchase order
    Odoo Material request for purchase tender Material request for tender
    Odoo Material request for manufacturing order.
    Odoo product request subassembly request raw material request order request
    Odoo manufacturing request purchase request purchase tender request internal transfer request
""",
    'author': 'BrowseInfo',
    "price": 65,
    "currency": "EUR",
    'website': 'https://www.browseinfo.com',
    'depends': ['base', 'sale_management', 'project', 'purchase', 'account', 'hr_timesheet', 'sale_stock',
                'stock',
                'hr_timesheet_attendance', 'bi_subtask', 'bi_material_purchase_requisitions', 'uom'],  #
    'data': [

        'security/ir.model.access.csv',
        'security/requisition_menu_hide.xml',
        'views/project_issue.xml',
        'views/project_project_views.xml',
        'views/res_partner_views.xml',

        'views/custom_job_costing_view.xml',
        'views/project_view.xml',
        'views/job_cost_view.xml',
        'views/material_view.xml',
        'views/configuration_view.xml',
        'report/job_cost_report.xml',
        'report/project_job_report_view.xml',
        'report/job_order_report_view.xml',
        'report/job_cost_sheet_report_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    "images": ['static/description/Banner.gif'],
    "live_test_url": 'https://youtu.be/xnjlNTuX6U4',
    'license': 'OPL-1',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
