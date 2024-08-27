# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Advanced Backend Theme for Community Edition',
    'version': '17.0.1.0.0',
    "category": "Themes/Backend",
    'live_test_url': 'https://youtu.be/R_LahYBKhMg',
    'sequence': 1,
    'summary': """
        Odoo Backend Theme, Odoo Community Backend Theme, Web backend Theme, Web Responsive Odoo Theme, New theme design, New design, Multi Level Menu,
        Web Responsive Odoo Backend Theme, Odoo Theme, Odoo Modern Theme, Odoo Modern Backend Theme Odoo, Advance Theme Backend Advanced, Sidebar Light,
        All in one, New advanced Odoo Menu, Sidebar apps, New design, Left sidebar menu, Web menu, Odoo backend menu, Web Responsive menu, Sidebar White,
        Advance Menu Odoo App Menu Apps, Advanced Apps Menu, Elegant Menu, Menuitem, Web App Menu Backend, Menu Odoo Backend, Collapse Menu, Light Sidebar,
        Expand Menu, Collapsed Menu, Expanded Menu, New Style Menus, Advanced Sidebar Menu, Advance Sidebar Menu, Responsive Menu Sidebar, Sidebar Theme,
        Responsive Sidebar, Hide menu, Show Menu, Hide Sidebar, Show Sidebar, Toggle Menu, Toggle Sidebar, All in one Dynamic Menu Access, Menu Theme,
        Visibility Menu Visibility, Quick Backend Menu, Dropdown Menu, Parent Menus, Shortcut Menus Shortcut, Menu Icons, Collapsible menu Odoo,
        Customize Menu Customize Sidebar App, Customization Menu Customization App Sidebar Customization Sidebar Apps, Group Left Menu in Odoo,
        Global Search Menu Search, Global Menu Access Global Apps Menu Global, Group Top Menu in Odoo, Odoo Foldable Menu Applications, Navbar,
        App web Menu, Quick Menu Access Menu, Menu Dynamic Sidebar, Any menu, Easy Access for menuitems, User Menu Users, All in one Sidebar,
        Advanced Menu, Advanced Odoo Menu Backend Odoo Web Theme Web Odoo, Elegant Theme Simple Theme, Advance List View Manager, Menu Style,
        Advanced List View Advanced Pivot View Theme Table View Theme Form View Theme Advanced Forms, Beautiful Theme Design, New Style Theme
    """,
    'description': "It's time to bid goodbye to the boring, monotonous interface of Odoo which you have been using for a while and say hello to a theme, which breathes life into your Odoo backend and one that you can customize and make new every day. We promises to be your one-time investment into Odoo Themes for sure.",
    'author': 'Innoway',
    'maintainer': 'Innoway',
    'price': '90.0',
    'currency': 'EUR',
    'website': 'https://innoway-solutions.com',
    'license': 'OPL-1',
    'images': [
        'static/description/wallpaper.png'
    ],
    'depends': [
        'web'
    ],
    'data': [
        
    ],
    'assets': {
        'web.assets_backend': [
            'neway_theme/static/src/scss/variable.scss',
            'neway_theme/static/src/scss/global.scss',
            'neway_theme/static/src/scss/menu.scss',
            'neway_theme/static/src/scss/control_panel.scss',
            'neway_theme/static/src/scss/searchpanel.scss',
            'neway_theme/static/src/scss/list.scss',
            'neway_theme/static/src/scss/form.scss',
            'neway_theme/static/src/scss/pivot.scss',
            'neway_theme/static/src/scss/activity.scss',
            'neway_theme/static/src/js/sidebar.js',
            'neway_theme/static/src/xml/sidebar.xml',
        ],
    },
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
        "static/src/xml/navbar.xml",
        "static/src/xml/sidebar.xml",
    ],
}
