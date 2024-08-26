##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2020 - Today O4ODOO (Omal Bastin)
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################
import ast

from odoo import api, fields, models
from odoo.osv import expression


# class AccountAccountTemplate(models.Model):
# 	_inherit = "account.account.template"
# 	
# 	parent_id = fields.Many2one('account.account.template', 'Parent Account', ondelete="set null")
# 	account_type = fields.Selection(selection_add=[('view', 'View')], ondelete={'view': 'cascade'})

# 	@api.model
# 	def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
# 		context = self._context or {}
# 		# updated to search the code too
# 		new_args = []
# 		if args:
# 			for arg in args:
# 				if isinstance(arg, (list, tuple)) and arg[0] == 'name' and isinstance(arg[2], str):
# 					new_args.append('|')
# 					new_args.append(arg)
# 					new_args.append(['code', arg[1], arg[2]])
# 				else:
# 					new_args.append(arg)
# 		# one Customer informed an issue that the same args is updated to company causing error
# 		# So to avoid that args was copied to new variable which solves the issue.
# 		if not context.get('show_parent_account',False):
# 			new_args = expression.AND([[('account_type', '!=', 'view')], new_args])
# 		return super(AccountAccountTemplate, self)._search(new_args, offset=offset, limit=limit,
# 														   order=order, count=count,
# 														   access_rights_uid=access_rights_uid)


class AccountAccount(models.Model):
	_inherit = "account.account"

	@api.depends('account_type')
	def _compute_internal_group(self):
		for account in self:
			if account.account_type:
				if account.account_type in ['view', 'off_balance']:
					account.internal_group = 'off_balance'
				else:
					account.internal_group = account.account_type.split('_')[0]

	@api.depends('code')
	def _compute_account_root(self):
		# this computes the first 2 digits of the account.
		# This field should have been a char, but the aim is to use it in a side panel view with hierarchy,
		# and it's only supported by many2one fields so far.
		# So instead, we make it a many2one to a psql view with what we need as records.
		# TODO now view accounts is not listed under the root view
		for record in self:
			if record.account_type != 'view':
				record.root_id = record.code and (ord(record.code[0]) * 1000 + ord(record.code[1:2] or '\x00')) or False
			else:
				record.root_id = False

	@api.depends('move_line_ids', 'move_line_ids.amount_currency', 'move_line_ids.debit', 'move_line_ids.credit')
	def compute_values(self):
		company_dict = {}
		target_currency = False
		if self._context.get('target_currency_id', False):
			target_currency = self.env['res.currency'].browse(self._context['target_currency_id'])
		for account in self:
			sub_accounts = self.with_context({'show_parent_account':True}).search([('id', 'child_of', [account.id])])
			balance = 0.0
			credit = 0.0
			debit = 0.0
			initial_balance = 0.0
			initial_deb = 0.0
			initial_cre = 0.0
			context = dict(self._context)
			context.update({'account_ids': sub_accounts})
			tables, where_clause, where_params = self.env['account.move.line'].with_context(context)._query_get()
			query1 = 'SELECT account_move_line.debit,account_move_line.credit,account_move_line.date,'\
					 'account_move_line.company_id FROM ' + tables + 'WHERE' + where_clause
			self.env.cr.execute(query1, tuple(where_params))
			for deb, cre, date, company_id in self.env.cr.fetchall():
				if company_id not in company_dict:
					company_dict[company_id] = self.env['res.company'].browse(company_id)
				if target_currency:
					deb = company_dict[company_id].currency_id._convert(deb, target_currency,
																		   company_dict[company_id], date)
					cre = company_dict[company_id].currency_id._convert(cre, target_currency,
																		   company_dict[company_id], date)

				balance += deb - cre
				credit += cre
				debit += deb
			account.balance = balance
			account.credit = credit
			account.debit = debit
			if context.get('show_initial_balance'):
				context.update({'initial_bal': True})
				tables, where_clause, where_params = self.env['account.move.line'].with_context(context)._query_get()
				query2 = 'SELECT account_move_line.debit,account_move_line.credit,account_move_line.date,' \
						 'account_move_line.company_id FROM ' + tables + 'WHERE' + where_clause
				self.env.cr.execute(query2, tuple(where_params))
				for deb, cre, date, company_id in self.env.cr.fetchall():
					if company_id not in company_dict:
						company_dict[company_id] = self.env['res.company'].browse(company_id)
					if target_currency:
						deb = company_dict[company_id].currency_id._convert(deb, target_currency,
																			company_dict[company_id], date)
						cre = company_dict[company_id].currency_id._convert(cre, target_currency,
																			company_dict[company_id], date)
					initial_cre += cre
					initial_deb += deb
				initial_balance += initial_deb - initial_cre
				account.initial_balance = initial_balance
			else:
				account.initial_balance = 0

	account_type = fields.Selection(selection_add=[('view', 'View')], ondelete={'view': 'cascade'})
	move_line_ids = fields.One2many('account.move.line', 'account_id', 'Journal Entry Lines')
	balance = fields.Float(compute="compute_values", digits=(16, 4), string='Balance')
	credit = fields.Float(compute="compute_values", digits=(16, 4), string='Credit')
	debit = fields.Float(compute="compute_values", digits=(16, 4), string='Debit')
	parent_id = fields.Many2one('account.account', 'Parent Account', ondelete="set null")
	child_ids = fields.One2many('account.account', 'parent_id', 'Child Accounts')
	parent_path = fields.Char(index=True, unaccent=False)
	initial_balance = fields.Float(compute="compute_values", digits=(16, 4), string='Initial Balance')

	_parent_name = "parent_id"
	_parent_store = True
	_parent_order = 'code, name'
	# _order = 'code, id'

	@api.model
	def _search(self, args, offset=0, limit=None, order=None, access_rights_uid=None):
		context = self._context or {}
		# updated to search the code too
		new_args = []
		if args:
			for arg in args:
				if isinstance(arg, (list, tuple)) and arg[0] == 'name' and isinstance(arg[2], str):
					new_args.append('|')
					new_args.append(arg)
					new_args.append(['code', arg[1], arg[2]])
				else:
					new_args.append(arg)
		# one Customer informed an issue that the same args is updated to company causing error
		# So to avoid that args was copied to new variable which solved the issue.
		if not context.get('show_parent_account', False):
			new_args = expression.AND([[('account_type', '!=', 'view')], new_args])
		return super(AccountAccount, self)._search(new_args, offset=offset, limit=limit, order=order,
												   access_rights_uid=access_rights_uid)

	
class AccountJournal(models.Model):
	_inherit = "account.journal"

	@api.model
	def _prepare_liquidity_account_vals(self, company, code, vals):
		res = super(AccountJournal, self)._prepare_liquidity_account_vals(company=company, code=code, vals=vals)
		account_code_prefix = ''
		if res['account_type'] == 'asset_cash':
			account_code_prefix = company.cash_account_code_prefix or company.bank_account_code_prefix or ''
		parent_id = self.env['account.account'].with_context({'show_parent_account': True}).search([
			('code', '=', account_code_prefix),
			('company_id', '=', company.id),
			('account_type', '=', 'view')], limit=1)
		if parent_id:
			res.update({'parent_id': parent_id.id})
		return res


class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	@api.model
	def _query_get(self, domain=None):
		self.check_access_rights('read')

		context = dict(self._context or {})
		domain = domain or []
		if not isinstance(domain, (list, tuple)):
			domain = ast.literal_eval(domain)
		#TODO check the use of include_initial_balance
		date_field = 'date'
		if context.get('aged_balance'):
			date_field = 'date_maturity'
		if context.get('date_to'):
			domain += [(date_field, '<=', context['date_to'])]
		if context.get('date_from'):
			if not context.get('strict_range'):
				domain += ['|', (date_field, '>=', context['date_from']),
						   ('account_id.include_initial_balance', '=', True)]
			elif context.get('initial_bal'):
				domain += [(date_field, '<', context['date_from'])]
			else:
				domain += [(date_field, '>=', context['date_from'])]

		if context.get('journal_ids'):
			domain += [('journal_id', 'in', context['journal_ids'])]

		state = context.get('state')
		if state and state.lower() != 'all':
			domain += [('parent_state', '=', state)]

		if context.get('company_id'):
			domain += [('company_id', '=', context['company_id'])]
		elif context.get('allowed_company_ids'):
			domain += [('company_id', 'in', self.env.companies.ids)]
		else:
			domain += [('company_id', '=', self.env.company.id)]

		if context.get('reconcile_date'):
			domain += ['|', ('reconciled', '=', False), '|',
					   ('matched_debit_ids.max_date', '>', context['reconcile_date']),
					   ('matched_credit_ids.max_date', '>', context['reconcile_date'])]

		if context.get('account_tag_ids'):
			domain += [('account_id.tag_ids', 'in', context['account_tag_ids'].ids)]

		if context.get('account_ids'):
			domain += [('account_id', 'in', context['account_ids'].ids)]

		if context.get('analytic_tag_ids'):
			domain += [('analytic_tag_ids', 'in', context['analytic_tag_ids'].ids)]

		if context.get('analytic_account_ids'):
			domain += [('analytic_account_id', 'in', context['analytic_account_ids'].ids)]

		if context.get('partner_ids'):
			domain += [('partner_id', 'in', context['partner_ids'].ids)]

		if context.get('partner_categories'):
			domain += [('partner_id.category_id', 'in', context['partner_categories'].ids)]

		where_clause = ""
		where_clause_params = []
		tables = ''
		if domain:
			domain.append(('display_type', 'not in', ('line_section', 'line_note')))
			domain.append(('parent_state', '!=', 'cancel'))

			query = self._where_calc(domain)

			# Wrap the query with 'company_id IN (...)' to avoid bypassing company access rights.
			self._apply_ir_rules(query)

			tables, where_clause, where_clause_params = query.get_sql()
		return tables, where_clause, where_clause_params


