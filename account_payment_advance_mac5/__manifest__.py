{
    'name': 'Advance Payments',
    'version': '17.0.2.0.3',
    'summary': """Advanced Payments, Advanced Down Payments or Advanced Deposits on Invoices,
Customer Invoice Advance Payments, Vendor Invoice Advance Payments,
Vendor Bill Advance Payments, Supplier Invoice Advance Payments, Odoo Advance Payments,
Odoo Advance Deposits""",
    'description': """
Advance Payments
================

This module creates advance payments with corresponding advance payment account. If advance payment
is applied to an invoice, it will create another Journal Entry for advance payment account and
partner's receivable/payable account.
""",
    'category': 'Accounting/Accounting',
    'author': 'MAC5',
    'contributors': ['MAC5'],
    'website': 'https://apps.odoo.com/apps/modules/browse?author=MAC5',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_advance_payment_invoice_views.xml',
        'views/res_config_views.xml',
        'views/account_account_views.xml',
        'views/account_payment_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [
        'static/description/apply_adv_payment_invoice2.png',
        'static/description/apply_adv_payment_invoice3.png',
        'static/description/apply_adv_payment_invoice4.png',
        'static/description/apply_adv_payment_invoice5.png',
        'static/description/apply_adv_payment_invoice.png',
    ],
    'price': 199.99,
    'currency': 'EUR',
    'support': 'mac5_odoo@outlook.com',
    'license': 'OPL-1',
    'live_test_url': 'https://youtu.be/ll8eNQiT0eo',
}
