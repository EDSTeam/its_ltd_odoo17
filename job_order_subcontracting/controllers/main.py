# -*- coding: utf-8 -*-

from collections import OrderedDict

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import get_records_pager, CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError

from odoo.osv.expression import OR


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'subcontractor_count' in counters:
            subcontractor_count = request.env['project.task'].search_count([
#                ('project_id.privacy_visibility', '=', 'portal'),
                ('is_subcontractor_joborder', '=', True),
                ('custom_contractor_partner_id', 'child_of', [request.env.user.partner_id.id])
            ])
            values['subcontractor_count'] = subcontractor_count
        return values

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        domain = [
#            ('project_id.privacy_visibility', '=', 'portal'),
            ('is_subcontractor_joborder', '=', True),
            ('custom_contractor_partner_id', 'child_of', [request.env.user.partner_id.id])
        ]
        values.update({
            'subcontractor_count': request.env['project.task'].search_count(domain)
        })
        return values

    @http.route(['/my/subcontractors', '/my/subcontractors/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_subcontractors(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None, search_in='content', **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        domain = [
#            ('project_id.privacy_visibility', '=', 'portal'),
            ('is_subcontractor_joborder', '=', True),
            ('custom_contractor_partner_id', 'child_of', [request.env.user.partner_id.id])
        ]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Title'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'project': {'label': _('Project'), 'order': 'project_id, stage_id'},#add
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'customer': {'input': 'customer', 'label': _('Search in Customer')},
            'stage': {'input': 'stage', 'label': _('Search in Stages')},
            'project': {'input': 'project', 'label': _('Search in Project')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        # extends filterby criteria with project (criteria name is the project id)
        projects = request.env['project.project'].search([('privacy_visibility', '=', 'portal')])
        for proj in projects:
            searchbar_filters.update({
                str(proj.id): {'label': proj.name, 'domain': [('project_id', '=', proj.id)]}
            })

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # archive groups - Default Group By 'create_date'
        # archive_groups = self._get_archive_groups('project.task', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]


        # search
        if search and search_in:
            search_domain = []
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in in ('customer', 'all'):
                search_domain = OR([search_domain, [('custom_contractor_partner_id', 'ilike', search)]])
            if search_in in ('message', 'all'):
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search)]])
            if search_in in ('stage', 'all'):
                search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
            domain += search_domain

        # task count
        subcontractor_count = request.env['project.task'].search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/subcontractors",
            url_args={
                'date_begin': date_begin,
                'date_end': date_end,
                'sortby': sortby,
                'filterby': filterby
            },
            total=subcontractor_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        tasks = request.env['project.task'].search(domain, order=order,
                                                   limit=self._items_per_page,
                                                   offset=pager['offset'])
        request.session['my_tasks_history'] = tasks.ids[:100]


        values.update({
            'date': date_begin,
            'date_end': date_end,
            'projects': projects,
            'tasks': tasks,
            'page_name': 'sub_tasks',
            # 'archive_groups': archive_groups,
            'default_url': '/my/subcontractors',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("job_order_subcontracting.portal_my_subcontractors", values)

    #@http.route(['/my/subcontractor/<int:task_id>'], type='http', auth="user", website=True)
    #def portal_my_subcontractor(self, task_id=None, **kw):
    #    task = request.env['project.task'].browse(task_id)
    #    vals = {
    #        'task_contract': task,
    #        'user': request.env.user
    #    }
    #    history = request.session.get('my_tasks_history', [])
    #    vals.update(get_records_pager(history, task))
    #    return request.render("job_order_subcontracting.portal_my_subcontractor", vals)

    def _custom_task_get_page_view_values(self, task, access_token, **kwargs):
        values = {
            'page_name': 'sub_tasks',
            'task_contract': task,
            'user': request.env.user
        }
        return self._get_page_view_values(task, access_token, values, 'my_tasks_history', False, **kwargs)

    @http.route(['/my/subcontractor/<int:task_id>'], type='http', auth="public", website=True)
    def portal_my_subcontractor(self, task_id, access_token=None, **kw):
        try:
            task_sudo = self._document_check_access('project.task', task_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        # ensure attachment are accessible with access token inside template
        for attachment in task_sudo.attachment_ids:
            attachment.generate_access_token()
        values = self._custom_task_get_page_view_values(task_sudo, access_token, **kw)
        return request.render("job_order_subcontracting.portal_my_subcontractor", values)
    
    # @http.route(['/my/subcontractor/<int:task_id>'], type='http', auth="user", website=True)
    # def portal_my_subcontractor(self, task_id, access_token=None, **kw):
    #     task = request.env['project.task'].browse(task_id)
    #     try:
    #         task_sudo = self._document_check_access('project.task', task_id, access_token)
    #     except (AccessError, MissingError):
    #         return request.redirect('/my')
            
    #     vals = {
    #         'task_contract': task,
    #         'user': request.env.user
    #     }
    #     history = request.session.get('my_tasks_history', [])
    #     vals.update(get_records_pager(history, task))
        
    #     return request.render("job_order_subcontracting.portal_my_subcontractor", vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
