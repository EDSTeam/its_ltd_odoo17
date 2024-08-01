# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################
from . import controller
from . import models
import odoo
from odoo import api, SUPERUSER_ID
import os
import logging
_logger = logging.getLogger(__name__)


def pre_init_check(cr):
	from odoo.service import common
	from odoo.exceptions import ValidationError
	from odoo import _
	
	version_info = common.exp_version()
	server_serie =version_info.get('server_serie')
	if server_serie != '17.0':
	    raise ValidationError(_('Module support Odoo series 17.0 found {}.'.format(server_serie)))


def _remove_dynamic_theme_assets(env):
	env['ir.attachment'].search(['|',('name', 'ilike', 'duotone'),('name', 'ilike', 'dynamic_variables')]).unlink()
	env['ir.asset'].search([('target', 'ilike', 'duotone')]).unlink()
    