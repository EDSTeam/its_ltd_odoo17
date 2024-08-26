# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Merge Purchase Orders",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "Purchases",
    "summary": """Merge PO App Merge Request For Quotation Merge RFQ Merge Requests For Quotations Combine Request For Quotation Combine Requests For Quotations Combine RFQ Module Combine Purchase Order Append PO Append Requests For Quotations Append Request For Quotation Append Purchase Order Merge Odoo""",
    "description": """
This module useful to Merge Purchase Orders.
Some time required to make a single quote from the multi quotation.
This module helps the user to merge quotations as well as many more options.
easy and quick solution to make
a new quotation or replace the existing quotation.
""",
    "version": "0.0.1",
    "depends": [
        "purchase",
        "stock",
    ],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "wizard/sh_merge_purchase_order_views.xml",
    ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
