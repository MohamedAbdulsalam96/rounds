# -*- coding: utf-8 -*-
# Copyright (c) 2015, Hemavatara dasa and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import *
from frappe.utils import get_datetime


class RoundsChanted(Document):
	def validate(self):
		if self.get('__islocal'):
			devotee = frappe.get_doc('Devotee', frappe.get_value('Devotee',{'user':self.devotee},'name'))
			if devotee:
				exist = frappe.db.sql("""
							select * from `tabRounds Chanted`
							where devotee=%s and date=%s""", (self.devotee, self.date), as_dict=True)

				if exist:
					frappe.throw("Rounds for %s already exist" % self.date)
				else:
					if self.minimum_number==None:
						self.minimum_number = devotee.daily_minimum_rounds

			else:
				frappe.throw("You are not registered as a devotee that can log rounds, please contact the system administrator")

		devotee = frappe.get_doc('Devotee', frappe.get_value('Devotee', {'user': self.devotee}, 'name'))

		chanted_today = float(self.beads) + float(self.clicker)/108
		self.total_chanted = chanted_today
		self.total_names = self.total_chanted * 16 * 108


@frappe.whitelist(allow_guest=False)
def update_balance(user):
	# frappe.msgprint(user)
	first = frappe.db.sql("""select name, _seen from `tabRounds Chanted`
    				where devotee=%s and start_here=0 order by date LIMIT 1""", (user), as_dict=False)
	start_here = 1
	if len(first) > 0:
		# frappe.msgprint(str(first))
		for d in first:
			round = frappe.get_doc('Rounds Chanted', d[0])
			if round:
				round.back_log = round.minimum_number - round.total_chanted

				if round.total_chanted > round.minimum_number:
					if round.openning_balance_chanted > 0:
						round.closing_balance_chanted = round.openning_balance_chanted + round.back_log
					else:
						round.back_log = 0
				else:
					round.closing_balance_chanted = round.openning_balance_chanted + round.back_log

				round.start_here = start_here
				round.closing_balance_names = round.openning_balance_names + round.total_names
				# frappe.msgprint(str(d))
				if d[1] !=None:
					round.updated = True

				round.save()

				closing_chanted = round.closing_balance_chanted
				closing_names = round.closing_balance_names
				date = frappe.utils.add_days(round.date,1)
				# frappe.msgprint(str(type(date)))
				# frappe.msgprint(str(type(datetime.today())))

				while True:
					if frappe.db.exists('Rounds Chanted', {'devotee': frappe.session.user, 'date': date}):
						round = frappe.get_doc('Rounds Chanted', frappe.get_value('Rounds Chanted', {'devotee': frappe.session.user, 'date': date}, 'name'))
						round.back_log = round.minimum_number - round.total_chanted
						round.openning_balance_chanted = closing_chanted
						round.openning_balance_names = closing_names
						if round.total_chanted > round.minimum_number:
							if round.openning_balance_chanted > 0:
								round.closing_balance_chanted = round.openning_balance_chanted + round.back_log
							else:
								round.back_log = 0
						else:
							round.closing_balance_chanted = round.openning_balance_chanted + round.back_log

						seen = frappe.db.sql("""select _seen from `tabRounds Chanted` where name=%s""", (round.name), as_dict=False)
						# frappe.msgprint(str(seen))
						if d[0] != None:
							round.updated = True

						round.closing_balance_names = round.openning_balance_names + round.total_names
						round.start_here = start_here
						round.save()

						closing_chanted = round.closing_balance_chanted
						closing_names = round.closing_balance_names
					else:
						round = frappe.new_doc("Rounds Chanted")
						# frappe.msgprint(round.devotee)
						round.devotee=frappe.session.user
						round.date = date
						round.beads=0
						round.clicker=0
						start_here = 0
						round.insert()

						# frappe.msgprint(round.devotee)

						round.back_log = round.minimum_number - round.total_chanted
						round.openning_balance_chanted = closing_chanted
						round.openning_balance_names = closing_names
						if round.total_chanted > round.minimum_number:
							if round.openning_balance_chanted > 0:
								round.closing_balance_chanted = round.openning_balance_chanted + round.back_log
							else:
								round.back_log = 0
						else:
							round.closing_balance_chanted = round.openning_balance_chanted + round.back_log

						round.closing_balance_names = round.openning_balance_names + round.total_names
						round.save()

						closing_chanted = round.closing_balance_chanted
						closing_names = round.closing_balance_names

					if date >= frappe.utils.getdate(frappe.utils.today()):
						break

					date = frappe.utils.add_days(date, 1)
					# frappe.msgprint(str(date))
			else:
				frappe.msgprint("Round not found")

	frappe.msgprint("Done")