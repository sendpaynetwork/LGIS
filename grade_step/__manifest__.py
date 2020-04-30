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
    'name': 'Administrative Employee Setup',
    'version': '1.1',
    'author': 'NNET ',
    'category': 'GRADE/STEP',
    'sequence': 21,
    'website': 'http://www.nigerianet.com',
    'summary': 'Staff Grade Level, Step and Salary Setup',
    'description': """
Administrative Setup Employee
===================================

This application enables you to manage  employee grade level and step...


You can manage:
---------------

* Salary Grade Level
* Grade Level Step
    """,
    'author': 'NigeriaNet LG',
    'website': 'http://www.nigerianet.com',
    'images': [

    ],
    'depends': ['hr_payroll', 'hr_contract', 'hr'],
    'data': [
        "views/grade_step_view.xml",
        "security/ir.model.access.csv"
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'css': ['static/src/css/lga.css'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
