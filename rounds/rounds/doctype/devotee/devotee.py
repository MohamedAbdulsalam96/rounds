# -*- coding: utf-8 -*-
# Copyright (c) 2015, Hemavatara dasa and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Devotee(Document):
	def validate(self):
		#frappe.msgprint(self.user)
		name = frappe.get_value('User', {'email': self.user}, 'name')
		#frappe.msgprint(name)
		user = frappe.get_doc('User', name)
		#frappe.msgprint(user.first_name)
		self.db_set('full_name', " ".join(filter(None, [user.first_name, user.middle_name, user.last_name])),
					update_modified=False)
		last = frappe.db.sql("""select closing_balance_names, date from `tabRounds Chanted`
	    				where devotee=%s order by date DESC LIMIT 1""", (self.user), as_dict=False)
		if len(last) > 0:
			for d in last:
				# devotee = devotee = frappe.get_doc('Devotee', frappe.get_value('Devotee',{'user':user},'name'))
				# devotee.target = target
				# frappe.msgprint(str(d))
				daily = self.daily_minimum_rounds*108*16
				remaining = long(self.target)-long(d[0])
				days = long(remaining)/long(daily)
				# frappe.msgprint(str(remaining) + " " +str(daily) + " " + str(days))
				self.reach_by = frappe.utils.add_days(frappe.utils.today(),days)
				self.balance_as_at = d[1]
				self.current_balance = d[0]


@frappe.whitelist(allow_guest=False)
def update_goal_date(user, target):
	last = frappe.db.sql("""select closing_balance_names from `tabRounds Chanted`
	    				where devotee=%s order by date DESC LIMIT 1""", (user), as_dict=True)
	start_here = 1
	if len(last) > 0:
		for d in last:
			devotee = devotee = frappe.get_doc('Devotee', frappe.get_value('Devotee',{'user':user},'name'))
			devotee.target = target
			daily = devotee.daily_minimum_rounds*108*16
			days = long(target-d)/long(daily)
			frappe.msgprint(str(target)+" " + str(daily) + " " + str(days))
			devotee.reach_by = frappe.utils.add_days(frappe.utils.today(),days)
			devotee.save()