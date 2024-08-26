# -*- coding: utf-8 -*-
# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Material Consumption on Job Order / Work Order',
    'currency': 'EUR',
    'license': 'Other proprietary',
    'price': 29.0,
    'summary': """Material Consumption on Job Order / Work Order""",
    'description': """
Job Order Material Consumption
Material Consumption on Job Order

job cost sheet
Odoo Job Costing And Job Cost Sheet (Contracting)
Odoo job cost sheet
job cost sheet odoo
contracting odoo
odoo construction
job costing (Contracting)
odoo job costing (Contracting)
odoo job costing Contracting
job order odoo
work order odoo
job Contracting
job costing
job cost Contracting
job costing
job cost sheet
cost sheet
project cost sheet
project planning
project sheet cost
job costing plan
Construction cost sheet
Construction job cost sheet
Construction jobs
Construction job sheet
Construction material
Construction labour
Construction overheads
Construction sheet plan
costing
workshop
job workshop
workshop
jobs
cost centers
odoo Contracting
Contracting odoo job

Construction Management
Construction Activity
Construction Jobs
Job Order Construction
Job Orders Issues
Job Order Notes
Construction Notes
Job Order Reports
Construction Reports
Job Order Note
Construction app
Construction 

    """,
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "http://www.probuse.com",
    'support': 'contact@probuse.com',
    # 'live_test_url': 'https://youtu.be/g4nT6gVyeqs',
    'live_test_url': 'https://probuseappdemo.com/probuse_apps/job_order_material_consumption/717',#'https://youtu.be/BQOqzLJ2zrA',
    'images': ['static/description/image1.png'],
    'version': '9.1.9',
    # 'category' : 'Operations/Project',
    'category': 'Inventory/Inventory',
    'depends': [
        'odoo_job_costing_management',
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/stock_picking_view.xml',
        'views/project_task_view.xml',
        'views/task_report_view.xml',
        'views/consumption_type_view.xml',
        'views/stock_move_views.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
