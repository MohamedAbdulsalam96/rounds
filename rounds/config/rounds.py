from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
    return [
		{
			"label": _("Rounds"),
			"items": [
				{
					"type": "doctype",
					"name": "Rounds Chanted"
				},
			]
		},
		{
			"label": _("Devotees"),
			"items": [
				{
					"type": "doctype",
					"name": "Devotee"
				},
			]
		},
	]