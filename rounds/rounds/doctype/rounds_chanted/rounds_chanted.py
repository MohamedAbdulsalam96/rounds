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
			devotee = frappe.get_doc('Devotee', frappe.get_value('Devotee',{'user':self.devotee},'name'))
			if devotee:
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
				else:
					# frappe.msgprint(str(devotee.daily_minimum_rounds))
					# frappe.msgprint(str(self.minimum_number))
					if self.minimum_number==None:
						self.minimum_number = devotee.daily_minimum_rounds

			else:
				frappe.throw("You are not registered as a devotee that can log rounds, please contact the system administrator")
		# rounds = float(self.clicker)/108
		# frappe.msgprint("Chanted: " + str(rounds))

		devotee = frappe.get_doc('Devotee', frappe.get_value('Devotee', {'user': self.devotee}, 'name'))
		# frappe.msgprint(str(devotee.daily_minimum_rounds))

		self.total_chanted = float(self.beads) + float(self.clicker)/108
		self.total_names = self.total_chanted*16*108

		# if self.minimum_number > self.total_chanted:
		self.back_log = self.total_chanted - self.minimum_number

		# else:
		# 	frappe.msgprint("Stored: "+self.devotee)

		#pass
		# name=frappe.get_value("Devotee",{'user':frappe.session.user},'name')
		# devotee = frappe.get_doc('Devotee', name)
		# frappe.msgprint(devotee.full_name)

		# # self.db_set('devotee_name',devotee.full_name,update_modified=False)