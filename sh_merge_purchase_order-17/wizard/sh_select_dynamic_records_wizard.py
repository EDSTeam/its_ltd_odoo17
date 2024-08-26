# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, _
from datetime import datetime

# Dynamic merge wizard
class SelectModelRecord(models.TransientModel):
    _name = 'sh.select.model.record.wizard'
    _description = 'SH Select Record to Merge Chatter Message'

    # Merge Chatter main method
    def sh_merge_chatter_message(self, record=None):
        if self.env.context.get('active_ids') and self.env.context.get('active_model'):
            active_ids = []
            Record = False

            active_ids = self.env.context.get('active_ids')
            active_ids = sorted(active_ids, reverse=True)

            check_messages = self.env['mail.message'].search(
                [('model', '=', self.env.context.get('active_model')), ('res_id', 'in', active_ids)], order="id desc")

            # for pass target record
            if record:
                Record = record

            if check_messages and Record:
                record_name = []

                message = '<b> ------------------------------------------------------------------------------------------------- <b/>'
                self.env['mail.message'].create({'res_id': Record.id,
                                                 'model': self.env.context.get('active_model'),
                                                 'body': message or False,
                                                 'message_type': 'comment',
                                                 })

                for current_record in active_ids:

                    messages_data = self.env['mail.message'].search(
                        [('model', '=', self.env.context.get('active_model')), ('res_id', '=', current_record)], order="id desc")

                    if messages_data:
                        for msg in messages_data:
                            new_msg = msg.copy()
                            new_msg.write({'res_id': Record.id,
                                           'date': datetime.now()
                                           })

                        record_id = self.env[self.env.context.get('active_model')].sudo().search(
                            [('id', '=', current_record)], limit=1, order="id desc")

                        if record_id and record_id.name:

                            message = _('This Message is From %s ',
                                        record_id._get_html_link())
                            record_name.append(
                                record_id.name)

                            self.env['mail.message'].create({'res_id': Record.id,
                                                             'model': self.env.context.get('active_model'),
                                                             'body': message or False,
                                                             'message_type': 'comment',
                                                             })

                message = '#------ '
                message += 'This Message is Generated From Merging Chatter Feature'

                record_name = sorted(record_name)

                if record_name:
                    message += '<b> %s <b/>' % ", ".join(record_name)

                message += ' ------#'

                self.env['mail.message'].create({'res_id': Record.id,
                                                 'model': self.env.context.get('active_model'),
                                                 'body': message or False,
                                                 'message_type': 'comment',
                                                 })
