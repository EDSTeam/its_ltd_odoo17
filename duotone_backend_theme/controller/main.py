# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
import re
import logging
from odoo.http import request
from odoo import http
from odoo.exceptions import ValidationError
from odoo.tools.mimetypes import get_extension
from werkzeug.wrappers import Response

_logger = logging.getLogger(__name__)

class WkTheme(http.Controller):

    @http.route(['/backend/theme_customize'], type='json', auth="public", website=True)
    def backend_theme_customize(self, get_bundle=False):
        if get_bundle:
            context = dict(request.context)
            return {
                'web.assets_backend': request.env["ir.qweb"].with_context(website_id=False)._get_asset_link_urls('web.assets_backend'),
            }
        return True

    @http.route(['/theme/backend/make_scss_custo'], type='json', auth='user', website=True)
    def backend_make_scss_custo(self, url, key, value, **kw):
        request.env['web_editor.assets'].make_scss_customization_backend(url, key, value, **kw)
        return True

    def _make_custom_image_file_url(self):
        return "duotone.custom_image"

    @http.route(['/create/image'], type='json', auth="public", website=True)
    def create_data(self, data, name, **kwargs):
        extension = get_extension(name) if name else ''
        if extension not in  ['.png','.jpg','.jpeg','.webp']:
            raise ValidationError("Please Choose Correct Image Format.")
        data = data.split(',')
        IrAttachment = request.env["ir.attachment"]
        custom_url = self._make_custom_image_file_url()
        custom_attachment = request.env['web_editor.assets']._get_custom_attachment(custom_url)
        datas = data[1]
        if custom_attachment:
            custom_attachment.sudo().unlink()
        new_attach = {
            'name': custom_url,
            'type': "binary",
            'datas': datas,
            # 'datas_fname': name.split(".")[0],
            'url': custom_url,
        }
        
        custom_attachment = IrAttachment.create(new_attach)
        request.session['theme_has_background_image']=custom_attachment.id
        return {
            'name': '/web/content/%s'%(custom_attachment.id),
            'id': custom_attachment.id
        }

    @http.route(['/duotone/remove/image'], type='json', auth="public", website=True)
    def remove_image(self, **kwargs):
        custom_url = self._make_custom_image_file_url()
        custom_attachment = request.env['web_editor.assets']._get_custom_attachment(custom_url)
        if custom_attachment:
            custom_attachment.sudo().unlink()
        return True

    @http.route(['/theme/data'], type='json', auth="public")
    def get_data(self, url, **kwargs):
        data = request.env['web_editor.assets'].get_scss_data(url).decode("utf-8")
        data = data[60: -18].split(',')
        value_dict = {}
        main_dict = {}
        for values in data:
            temp_dict = {}
            arr_data = values.split(':')
            temp_dict[re.sub(r"[\n\t\s]*", "", arr_data[0])[1:-1]] = str(re.sub(r"[\n\t\s]*", "", arr_data[-1]))
            value_dict.update(temp_dict)
        main_dict['background_color'] = value_dict.get('background_color', '#474747')
        main_dict['foreground_color'] = value_dict.get('foreground_color', '#F77DBA')
        main_dict['font'] = value_dict.get('font', "'Lato'")
        bck_img = value_dict.get('bck_img')
        main_dict['bck_img'] = 0 if bck_img == 'null' else bck_img
        main_dict['opacity'] = value_dict.get('opacity', 1)
        main_dict['btn_type'] = value_dict.get('btn_type', 1)
        return main_dict