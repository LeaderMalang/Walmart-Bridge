 # -*- coding: utf-8 -*-
##############################################################################
#       
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 webkul
#    Author :
#               www.webkul.com  
#
##############################################################################

from odoo import api, fields, models, tools, SUPERUSER_ID, _
import odoo.addons.decimal_precision as dp
from odoo.tools.translate import _
from odoo import tools
import time
#import openerp.pooler
import odoo.netsvc

from datetime import date
from odoo.exceptions import UserError, AccessError
    
class message_wizard(models.TransientModel):
    _name = "message.wizard"
    
    text = fields.Text('Message' ,readonly=True ,translate=True)
             




