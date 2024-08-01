# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
import re
import base64
import logging





from odoo import models, api


_logger = logging.getLogger(__name__)

class Assets(models.AbstractModel):
    _inherit = 'web_editor.assets'

    def save_asset_backend(self, url, bundle, content, file_type):
        """
        Customize the content of a given asset (scss / js).

        Params:
            url (src):
                the URL of the original asset to customize (whether or not the
                asset was already customized)

            bundle_xmlid (src):
                the name of the bundle in which the customizations will take
                effect

            content (src): the new content of the asset (scss / js)

            file_type (src):
                either 'scss' or 'js' according to the file being customized
        """
        custom_url = self._make_custom_asset_url(url, bundle)
        datas = base64.b64encode((content or "\n").encode("utf-8"))

        # Check if the file to save had already been modified
        custom_attachment = self._get_custom_attachment(custom_url)
        if custom_attachment:
            # If it was already modified, simply override the corresponding
            # attachment content
            custom_attachment.write({"datas": datas})
        else:
            # If not, create a new attachment to copy the original scss/js file
            # content, with its modifications
            new_attach = {
                'name': url.split("/")[-1],
                'type': "binary",
                'mimetype': (file_type == 'js' and 'text/javascript' or 'text/scss'),
                'datas': datas,
                'url': custom_url,
            }
            # new_attach.update(self._save_asset_attachment_hook())
            new_attach.update(self._save_asset_hook())
            self.env["ir.attachment"].create(new_attach)
            # Create an asset with the new attachment
            IrAsset = self.env['ir.asset']
            new_asset = {
                'path': custom_url,
                'target': url,
                'directive': 'replace',
                **self._save_asset_hook(),
            }
            target_asset = self._get_custom_asset(url)[0]
            if target_asset:
                new_asset['name'] = target_asset.name + ' override'
                new_asset['bundle'] = target_asset.bundle
                new_asset['sequence'] = target_asset.sequence
            else:
                new_asset['name'] = '%s: replace %s' % (bundle, custom_url.split('/')[-1])
                new_asset['bundle'] = IrAsset._get_related_bundle(url, bundle)
            IrAsset.create(new_asset)
            # view_id.website_id = False

        self.env.registry.clear_cache()

            
    def _generate_updated_file_content(self, updatedFileContent, name, value):
        pattern = "'%s': %%s,\n" % name
        regex = re.compile(pattern % ".+")
        replacement = pattern % value
        if regex.search(updatedFileContent):
            updatedFileContent = re.sub(regex, replacement, updatedFileContent)
        else:
            updatedFileContent = re.sub(r'( *)(.*hook.*)', r'\1%s\1\2' % replacement, updatedFileContent)
        return updatedFileContent

    @api.model
    def make_scss_customization_backend(self, url, key, value, **kw):
        """
        Makes a scss customization of the given file. That file must
        contain a scss map including a line comment containing the word 'hook',
        to indicate the location where to write the new key,value pairs.

        Params:
            url (str):
                the URL of the scss file to customize (supposed to be a variable
                file which will appear in the assets_frontend bundle)

            values (dict):
                key,value mapping to integrate in the file's map (containing the
                word hook). If a key is already in the file's map, its value is
                overridden."""
        custom_url = self._make_custom_asset_url(url, 'web.assets_backend')
        updatedFileContent = self._get_content_from_url(custom_url) or self._get_content_from_url(url)
        updatedFileContent = updatedFileContent.decode('utf-8')
        if kw.get('google_fonts'):
            values = kw
            values[key] = value
            for name, value in values.items():
                pattern = "'%s': %%s,\n" % name
                regex = re.compile(pattern % ".+")
                replacement = pattern % value
                if regex.search(updatedFileContent):
                    updatedFileContent = re.sub(regex, replacement, updatedFileContent)
                else:
                    updatedFileContent = re.sub(r'( *)(.*hook.*)', r'\1%s\1\2' % replacement, updatedFileContent)
        else:
            updatedFileContent = self._generate_updated_file_content(updatedFileContent, key, value)
        
        self.save_asset_backend(url, 'web.assets_backend', updatedFileContent, 'scss')

        return True


    def get_scss_data(self, url):
        custom_url = self._make_custom_asset_url(url, 'web.assets_backend')
        updatedFileContent = self._get_content_from_url(custom_url) or self._get_content_from_url(url)
        return updatedFileContent