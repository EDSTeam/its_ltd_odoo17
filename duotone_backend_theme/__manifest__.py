# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
    "name":  "Theme Duotone : Backend Theme",
    "summary":  """Odoo Theme Duotone: Backend Theme consists wide range of things, such as font types, colors, buttons, background images/transparency and other areas that affect the aesthetics of your site""",
    "category":  "Theme/Backend",
    "version":  "1.0.0",
    "author":  "Webkul Software Pvt. Ltd.",
    "license":  "Other proprietary",
    "website":  "https://store.webkul.com/odoo-theme-duotone-backend-theme.html",
    "description":  """Theme Duotone: Backend Theme
Duotone
Backend Theme
Odoo Theme
Odoo Duotone
Odoo Theme Duotone
Odoo Backend Theme Duotone
Duotone Odoo
Odoo Theme Duotone: Backend Theme
duotone_backend_theme
Duotone backend theme""",
    "live_test_url":  "http://odoodemo.webkul.com/?module=duotone_backend_theme",
    "depends":  [
        'web',
        'web_editor',
    ],
    "data":  [
            'data/ir_asset.xml',
            'views/templates.xml',
            ],

    "images":  [
        'static/description/Banner.png',
        'static/description/main-Banner.png',
    ],
    "application":  False,
    "installable":  True,
    "price":  129,
    "currency":  "USD",
    "pre_init_hook":  "pre_init_check",
    'uninstall_hook': '_remove_dynamic_theme_assets',
}
