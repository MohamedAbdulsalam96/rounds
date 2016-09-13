# -*- coding: utf-8 -*-
# Copyright (c) 2015, Hemavatara dasa and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RoundsChanted(Document):
	def validate(self):
		#pass
		if self.get('__islocal'):
			# frappe.msgprint(self.devotee)
			# frappe.msgprint(self.date)

			exist = frappe.db.sql("""
						select * from `tabRounds Chanted`
						where devotee=%s and date=%s""", (self.devotee, self.date), as_dict=True)

			if exist:
				# frappe.msgprint("Exists: " + exist[0]["name"])
				frappe.throw("Rounds for this date already exist")
			# exists = frappe.get_doc({
			# 			"doctype": "Rounds Chanted",
			# 			"devotee": self.devotee,
			# 			"date": self.date
			# 		})

		# else:
		# 	frappe.msgprint("Stored: "+self.devotee)

		#pass
		# name=frappe.get_value("Devotee",{'user':frappe.session.user},'name')
		# devotee = frappe.get_doc('Devotee', name)
		# frappe.msgprint(devotee.full_name)

		# # self.db_set('devotee_name',devotee.full_name,update_modified=False)