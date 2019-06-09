# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Rounds",
			"category" : "Modules",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Rounds"),
			"type":"module",
			"description":"Manage you rounds chanted."
		}
	]
