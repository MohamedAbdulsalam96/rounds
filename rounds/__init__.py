# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = '0.0.1'

@frappe.whitelist(allow_guest=False)
def reset_round_seen(name):
    round = frappe.get_doc("Rounds Chanted", name)
    round.reset_seen
    frappe.msgprint(round._seen)