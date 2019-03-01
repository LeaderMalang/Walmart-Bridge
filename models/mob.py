# -*- coding: utf-8 -*-
# #############################################################################
# 
# ##############################################################################

import http.client
import urllib
import csv
import re
import random
import logging
import requests
import uuid
import base64
import time
from functools import wraps
from uuid import uuid4
from lxml import etree
from lxml.builder import E, ElementMaker
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

#import odoo.pooler
import odoo.netsvc
from odoo import api, fields, models, tools, SUPERUSER_ID, _


import os
from odoo.exceptions import UserError
from odoo import tools
from odoo.tools.translate import _
from odoo.tools.safe_eval import safe_eval as eval
import odoo.addons.decimal_precision as dp
from odoo.tools.float_utils import float_round
from odoo.tools import config

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


logger = logging.getLogger(__name__)

PRIVATE_KEY = 'MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAKXOTWVZJDNhVaAt8Yt468TQ2+evkLT7ZBgr9pZ3xFSUM9e7cdvlxdYHIFYz5fQlXwXe0J9JnMnFE9dajr8ibrsGgCvSiD0IxpNKy/IW1xUMxSCUP8sUSCjSLlNrdWId2dP7ZjOq1f38kYY8620t/cio+cEU8ZbVllF32MpFu/eVAgMBAAECgYBg3fY5j6qmmeb8fdrwMOUNRzgyU0+nbHc95/FYVwBMqYjgMJKEdeju8Zriwc9Go86wD0yywr7m4kyFNFLRN7yYdgvoZcV3kCI2GmZi4n5ycnBhpk0IIi3V8ro3kvqLqQunx6L8ptCFvctZr6uz2M005d3AmBTS6JjeJM3NNjv6wQJBAN0/h4B6pDL9fklOU96quojLmSQKXwRa9tT5EhU90rDOvy6kZ98Q96YfRoLCBV4ZMmIlP6IkT0o6JKESzdB51icCQQC/2Wr3/cgwcCQcyzIckFh6HSAowXe6aSEVK47qQui6qTCzApiznIC7iKoY6KjulrjPbJYOa21unGydI5Q72zXjAkBFLtFjNnZTz3qG16xYK1DK58dKQsf1Z7BZZkzmQX+5c9zKa/RjBz45PvxgdOUSyJQ9pmIghHQaxNWhXGzpLL/vAkB8a73i/XTCbUgOYH2sZrTq5U7A/8/tVlb9StWR+jjDLg0GW427FqmqdhSSuPkuWxOaenrK+ULsdIhAVR3CwAUvAkB+Jd6iVANKh6i84bW9Zk66S1RKsP0Y0dqw0Ynegnah0cUhsC7tmj5nU0mnXVj17XPmonMPnQbzWeTSYYBo8fAW' 


class walmart_configure(models.Model):
    _name = "walmart.configure"
    _inherit = ['mail.thread']
    _description = "Walmart Configuration"
    
    

    name = fields.Char('Base URL', required=True, size=255, index=True)
    user = fields.Char('API Consumer Id', required=True, size=100)
    pwd = fields.Char('API Consumer Channel Type', required=True, size=100)
    status = fields.Char('Connection Status', readonly=True, size=255)
    active = fields.Boolean('Active', default=True)
    credential = fields.Boolean('Show/Hide Credentials Tab',
                                     help="If Enable, Credentials tab will be displayed, \
                                     And after filling the details you can hide the Tab.")
    auto_invoice = fields.Boolean('Auto Invoice',
                                       help='If Enabled, Order will automatically Invoiced \
                                       on Magento when OpenERP order Get invoiced.', default=True)
    auto_ship = fields.Boolean('Auto Shipment',
                                    help='If Enabled, Order will automatically shipped \
                                    on Magento when OpenERP order Get Delivered.', default=True)
    create_date = fields.Datetime('Created Date')
    template_id = fields.Many2one('product.template', 'Template')
    
   
   
    
    
        
        
   
    @api.multi
    def write(self, vals):
        active_ids = self.env['walmart.configure'].search([('active', '=', True)])
        if vals:
            if len(active_ids) > 1:
                raise UserError(_("Sorry, Only one active connection is allowed."))
        return super(walmart_configure, self).write(vals)
        

    # ############################################
    # #         walmart connection             ##
    # ############################################
    
        # ############################################
    # #         walmart connection             ##
    # ############################################
    
    #~ def get_sign(self, url, method, timestamp):
        #~ return self.sign_data(
            #~ '\n'.join([self.user, url, method, timestamp]) + '\n'
        #~ )

    #~ def sign_data(self, data):
        #~ rsakey = RSA.importKey(base64.b64decode(PRIVATE_KEY))
        #~ signer = PKCS1_v1_5.new(rsakey)
        #~ digest = SHA256.new()
        #~ digest.update(data.encode('utf-8'))
        #~ sign = signer.sign(digest)
        #~ return base64.b64encode(sign)

    def get_headers(self, channel_type, consumer_id):
        return {
            'wm_consumer.channel.type': channel_type,
            'wm_consumer.id': consumer_id,
            'Accept': 'application/xml'
        }
    
    def send_request(self, method, url, params=None, body=None, request_headers=None):
        
        url = self.name 
        consumer_id = self.user
        channel_type = self.pwd
        session = 0
        session = requests.Session()
        encoded_url = url
        if params:
            encoded_url += '?%s' % urlencode(params)
        headers = self.get_headers(channel_type, consumer_id)
        if request_headers:
            headers.update(request_headers)

        if method == 'GET':
            return session.get(url, params=params, headers=headers)
        elif method == 'PUT':
            return session.put(
                url, params=params, headers=headers, data=body
            )
        elif method == 'POST':
            return session.post(url, data=body, headers=headers)
            

    def test_connection(self):
        obj = self
        url = obj.name 
        consumer_id = obj.user
        channel_type = obj.pwd
        headers = self.get_headers(channel_type, consumer_id)
        
        
        res = requests.get(str(url)+"/proxy/item-api-doc-app/rest/v3/feeds?includeDetails=false&offset=0&limit=50", headers=headers)
         
            
        if res.status_code==200:
            text = 'Test Connection with walmart is successful, now you can proceed with synchronization.'
            status = "Congratulation, It's Successfully Connected with Walmart Api."
        else:
            status = str(res.status_code) + " Please check your Api details."  
            text = str(res.status_code) + " Please check your Api details."  
               
        self.write({'status': status})
        partial = self.env['message.wizard'].create({'text': text})
        return {'name': _("Information"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'message.wizard',
                'res_id': partial.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
        }    

        
    



class walmart_synchronization(models.Model):
    _name = "walmart.synchronization"
    
    configuration = fields.Many2one('walmart.configure', 'Walmart Configuration')
    name = fields.Char('Name', default='Synchronization')




    def update_inventory(self):
       
        return self.connection.send_request(
            method='PUT',
            url=self.configuration.name,
            params={'sku': 'MTS-R4R-2XL'},
            body=self.get_inventory_payload('MTS-R4R-2XL', '10'),
            request_headers=None
        )
        

    def get_inventory_payload(self, sku, quantity):
        element = ElementMaker(
            namespace='http://walmart.com/',
            nsmap={
                'wm': 'http://walmart.com/',
            }
        )
        return etree.tostring(
            element(
                'inventory',
                element('sku', sku),
                element(
                    'quantity',
                    element('unit', 'EACH'),
                    element('amount', str(quantity)),
                ),
                element('fulfillmentLagTime', '4'),
            ), xml_declaration=True, encoding='utf-8'
        )
        
        
    def syn_inventory(self):
        
        return True     
        
    def syn_product(self):
        
        return True  


