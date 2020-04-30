# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Administrative Setup for Local Govt',
    'version': '1.1',
    'author': 'NNET ',
    'category': 'State/LGA',
    'sequence': 21,
    'website': 'http://www.sendpaynetwork.com',
    'summary': 'Country, State, Local Govt Details',
    'description': """
Administrative Setup for Local Govt
===================================

This application enables you to manage local govt aspects of your states...


You can manage:
---------------
* Local Govt Code
* State ID Departments
* Local Govt
* Salary Grade Level
* Grade Level Step
    """,
    'author': 'SendPay Network LG',
    'website': 'http://www.sendpaynetwork.com',
    'images': [

    ],
    'depends': [],
    'data': [
        "views/lga_view.xml",
        "security/ir.model.access.csv",
        #"security/state_lga_security.xml",
    ],
    'update_xml': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'css': ['static/src/css/lga.css'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
