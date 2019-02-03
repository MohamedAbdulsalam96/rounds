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
		if self.is_new():
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

		day_before = frappe.utils.add_days(self.date,-1)
		
		last_round = frappe.db.sql("""
						select name from `tabRounds Chanted`
						where devotee=%s and date=%s""", (self.devotee, day_before), as_dict=False)

		chanted_today = float(self.beads) + float(self.clicker)/108
		self.total_chanted = chanted_today
		self.total_names = self.total_chanted * 16 * 108
		self.back_log = self.total_chanted-self.minimum_number

		if len(last_round)>0:
			for d in last_round:
				round = frappe.get_doc('Rounds Chanted', d[0])
				self.openning_balance_chanted = round.closing_balance_chanted
				self.openning_balance_names = round.closing_balance_names
				if self.total_chanted >= self.minimum_number:
					self.days_in_a_row_max = round.days_in_a_row_max + 1
				else:
					self.days_in_a_row_max = 0
					self.days_in_a_row_min = round.days_in_a_row_min + 1
		else:
			self.openning_balance_chanted = 0
			self.openning_balance_names = 0
			if self.total_chanted >= self.minimum_number:
					self.days_in_a_row_max = 1
			else:
				self.days_in_a_row_max = 0
				self.days_in_a_row_min = 1
		
		if self.reset_to_zero==True:
			self.openning_balance_names = 0

		if (self.openning_balance_chanted - self.back_log) <=0:
			self.closing_balance_chanted =  0
		else:
			self.closing_balance_chanted =  self.openning_balance_chanted - self.back_log		
		
		
		self.closing_balance_names = self.openning_balance_names + self.total_names
		
		

@frappe.whitelist(allow_guest=False)
def update_balance(user):
	# frappe.msgprint(user)
	first = frappe.db.sql("""select name, _seen from `tabRounds Chanted`
    				where devotee=%s and updated=1 order by date ASC LIMIT 1""", (user), as_dict=False)

	# frappe.msgprint(str(len(first)))
	if len(first) == 0:
		first = frappe.db.sql("""select name, _seen from `tabRounds Chanted`
	        				where devotee=%s order by date DESC LIMIT 1""", (user), as_dict=False)

	if len(first) ==0:
		round = frappe.new_doc("Rounds Chanted")
		# frappe.msgprint(round.devotee)
		round.devotee = frappe.session.user
		round.date = frappe.utils.today()
		round.beads = 0
		round.clicker = 0
		round.insert()
	else:
		# frappe.msgprint(str(first))
		for d in first:
			round = frappe.get_doc('Rounds Chanted', d[0])
			if round:
				round.back_log = round.minimum_number - round.total_chanted
				if round.reset_to_zero == True:
					#round.openning_balance_chanted = 0
					round.openning_balance_names = 0
					
				# frappe.msgprint(str(round.date))
				if round.total_chanted > round.minimum_number:
					if round.openning_balance_chanted > 0:
						round.closing_balance_chanted = round.openning_balance_chanted - round.back_log
					else:
						round.back_log = 0
				else:
					round.closing_balance_chanted = round.openning_balance_chanted - round.back_log

				if round.closing_balance_chanted <0:
					round.closing_balance_chanted=0

				round.closing_balance_names = round.openning_balance_names + round.total_names
				# frappe.msgprint(str(d))
				# if d[1] !=None:
					# round.updated = True

				if round.days_in_a_row_max == None:
					round.days_in_a_row_max = 0

				if round.days_in_a_row_min == None:
					round.days_in_a_row_min = 0


				date = frappe.utils.add_days(round.date, -1)
				exists = frappe.db.exists('Rounds Chanted', {'devotee': frappe.session.user, 'date': date})
				if exists:
					previous_round = frappe.get_doc('Rounds Chanted', exists)
					if round.total_chanted >= round.minimum_number:
						round.days_in_a_row_min = 0
						round.days_in_a_row_max = previous_round.days_in_a_row_max + 1
					else:
						round.days_in_a_row_min = previous_round.days_in_a_row_min + 1
						round.days_in_a_row_max = 0
				else:
					if round.total_chanted >= round.minimum_number:
						round.days_in_a_row_min = 0
						round.days_in_a_row_max = round.days_in_a_row_max + 1
					else:
						round.days_in_a_row_min = round.days_in_a_row_min + 1
						round.days_in_a_row_max = 0

				rounds_max = round.days_in_a_row_max
				rounds_min = round.days_in_a_row_min
				round.updated = 0
				round.save()

				closing_chanted = round.closing_balance_chanted
				closing_names = round.closing_balance_names
				date = frappe.utils.add_days(round.date, 1)

				count = 0
				while True:
					count = count + 1
					# frappe.msgprint("loop " + str(round.date))
					if frappe.db.exists('Rounds Chanted', {'devotee': frappe.session.user, 'date': date}):
						round = frappe.get_doc('Rounds Chanted', frappe.get_value('Rounds Chanted', {'devotee': frappe.session.user, 'date': date}, 'name'))
						round.back_log = round.minimum_number - round.total_chanted
						round.openning_balance_chanted = closing_chanted
						round.openning_balance_names = closing_names

						if round.days_in_a_row_max == None:
							round.days_in_a_row_max=0

						if round.days_in_a_row_min == None:
							round.days_in_a_row_min = 0

						if round.total_chanted > round.minimum_number:
							if round.openning_balance_chanted > 0:
								round.closing_balance_chanted = round.openning_balance_chanted - round.back_log
							else:
								round.back_log = 0
						else:
							round.closing_balance_chanted = round.openning_balance_chanted - round.back_log

						if round.total_chanted >= round.minimum_number:
							round.days_in_a_row_min = 0
							round.days_in_a_row_max = rounds_max + 1
						else:
							round.days_in_a_row_min = rounds_min + 1
							round.days_in_a_row_max = 0

						if round.closing_balance_chanted < 0:
							round.closing_balance_chanted = 0

						round.closing_balance_names = round.openning_balance_names + round.total_names
						rounds_max = round.days_in_a_row_max
						rounds_min = round.days_in_a_row_min
						round.updated = 0
						round.save()

						closing_chanted = round.closing_balance_chanted
						closing_names = round.closing_balance_names
					else:
						if date > frappe.utils.getdate(frappe.utils.today()):
							break
						round = frappe.new_doc("Rounds Chanted")
						# frappe.msgprint(round.devotee)
						round.devotee=frappe.session.user
						round.date = date
						round.beads=0
						round.clicker=0
						round.insert()

						# frappe.msgprint(round.devotee)

						round.back_log = round.minimum_number - round.total_chanted
						round.openning_balance_chanted = closing_chanted
						round.openning_balance_names = closing_names
						if round.total_chanted > round.minimum_number:
							if round.openning_balance_chanted > 0:
								round.closing_balance_chanted = round.openning_balance_chanted - round.back_log
							else:
								round.closing_balance_chanted = 0
						else:
							round.closing_balance_chanted = round.openning_balance_chanted - round.back_log

						if round.total_chanted >= round.minimum_number:
							round.days_in_a_row_min = 0
							round.days_in_a_row_max = rounds_max + 1
						else:
							round.days_in_a_row_min = rounds_min + 1
							round.days_in_a_row_max = 0

						if round.closing_balance_chanted < 0:
							round.closing_balance_chanted = 0

						round.closing_balance_names = round.openning_balance_names + round.total_names
						round.updated = 0
						round.save()

						closing_chanted = round.closing_balance_chanted
						closing_names = round.closing_balance_names
						rounds_max = round.days_in_a_row_max
						rounds_min = round.days_in_a_row_min

					date = frappe.utils.add_days(date, 1)
					if date > frappe.utils.getdate(frappe.utils.today()):
						break
					
					if count>100:
						round.updated = 1
						round.save()
						break
					# frappe.msgprint(str(date))
			else:
				frappe.msgprint("Round not found")


@frappe.whitelist(allow_guest=False)
def update_all_devotees():
	# frappe.msgprint("Running")
	devotees = frappe.get_all('Devotee',fields=['user'])#,ignore_permissions=True)
	for d in devotees:
		update_balance(d['user'])