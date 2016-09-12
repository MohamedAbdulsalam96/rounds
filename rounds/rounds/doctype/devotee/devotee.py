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

