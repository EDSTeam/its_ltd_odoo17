# Copyright (C) Softhealer Technologies.
{
    'name': 'Bundle Product Management',
    'author': 'Softhealer Technologies',
    'website': "https://www.softhealer.com",
    "support": "support@softhealer.com",
    'version': '0.1',
    "license": "OPL-1",
    'category': 'Extra Tools',
    "summary": "Product Pack Combo Products Bunch Products All In One Products Product Package Product Combo Product Bundle Mass Products On Shop Multiple Products website product kit pos product pack pos bundle all in one product bundle Odoo Odoo App Bundle product delivery Bundle delivery pack Sale Combo of Product Bundle of products Pack of Products Combined Product Pack  combine two or more product pack",
    "description": """
Do you want to make a combo of several products? In competitive market prices play an important role. This module is useful for creating a pack of some products in sales, purchase, inventory & invoice. You can generate a product bundle for selling multi-products at once. You can make a bunch of several products and easily enhance your sailing.
 All In One Product Bundle Odoo, Product Pack Odoo, Combo Products Odoo
Bunch Products Module, All In One Products, Generate Product Package, Manage Product Combo, Fix Particular Product Bundle,Give Product Pack, Mass Products, Add Multiple Products Odoo. 
 Bunch Products, All In One Products App, Product Package, Product Combo Module, Particular Product Bundle, Product Pack, Mass Products, Add Multiple Products, Multiple Products In Pack, Make Product Bunch Odoo.""",
    'depends': ['sale_management', 'purchase', 'stock', 'account', 'sh_base_bundle'],
    'data': [
        'security/ir.model.access.csv',
        'views/sh_sale_order_view.xml',
        'views/sh_purchase_order_view.xml',
        'views/sh_account_invoice_view.xml',
        'views/sh_stock_picking_view.xml',
        'wizard/sh_product_bundle_wizard_view.xml',
    ],
    'images': ['static/description/background.png', ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 35,
    "currency": "EUR"
}
