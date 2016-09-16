# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe, json

__version__ = '0.0.1'

@frappe.whitelist(allow_guest=False)
def reset_round_seen(name):
    # seenby = '["' + frappe.session.user + '"]'
    # sql = """UPDATE `tabRounds Chanted` set _seen = '%s' where name='%s'""" % (seenby,name)
    # #seenby.append(str(frappe.session.user))
    # round = frappe.db.sql(sql, as_dict=True)
    # return len(round)#sql
    round = frappe.get_doc("Rounds Chanted", name)
    round.add_seen()
