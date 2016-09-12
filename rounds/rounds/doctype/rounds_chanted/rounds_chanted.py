# -*- coding: utf-8 -*-
# Copyright (c) 2015, Hemavatara dasa and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RoundsChanted(Document):
	def validate(self):
		name=frappe.get_value("Devotee",{'user':frappe.session.user},'name')
		devotee = frappe.get_doc('Devotee', name)
		frappe.msgprint(frappe.session.user)
		frappe.msgprint(devotee.full_name)
		self.db_set('devotee', devotee, update_modified=False)
		self.db_set('devotee_name',devotee.full_name,update_modified=False)