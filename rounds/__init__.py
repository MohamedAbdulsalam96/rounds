# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe, json

__version__ = '0.0.1'

@frappe.whitelist(allow_guest=False)
def reset_round_seen(name):
    round = frappe.get_doc("Rounds Chanted", name)
    return json.loads(round._seen)