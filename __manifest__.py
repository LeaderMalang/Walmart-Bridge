# -*- coding: utf-8 -*-
# #############################################################################
#
#   OpenERP, Open Source Management Solution
#    Copyright (C) 2013 webkul
#	 Author :
#				www.webkul.com	
#
##############################################################################
{
    'name': 'Walmart Odoo Bridge',
    'version': '11.0.0.1',
    'category': 'Generic Modules',
    'sequence': 1,
    'summary': 'Basic WOB',
    'description': """
Walmart Odoo Bridge (WOB)
============================
This Brilliant Module will Connect Odoo with Walmart and synchronise all of your item, order, product, inventory
---------------------------------------------------------------------------------------------------------------


Some of the brilliant feature of the module:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	
	
	1. synchronise product inventory of catelog products.
	
	2. synchronise order of catelog products.
	
This module works very well with latest version of walmart and latest version of Odoo 11
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """,
    'author': 'charles@dynexcel.com',
    'website': 'http://dynexcel.com',
    'depends': [
        'sale',
        'stock',
        'account',
        'delivery',
    ],
    'data': [
        'wizard/message_wizard_view.xml',
        #'wizard/status_wizard_view.xml',
        #'views/mob_sequence.xml',
        'views/mob_view.xml',
        #'views/mob_data.xml',
        #'views/product_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
