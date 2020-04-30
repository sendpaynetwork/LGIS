# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Employee Contracts Extension',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Add all information on the employee form to manage contracts.
=============================================================

    * Contract
    * Place of Birth,
    * Medical Examination Date
    * Company Vehicle

You can assign several contracts per employee.
    """,
    'website': 'https://www.odoo.com/page/employees',
    'depends': ['hr_contract', 'employee_union'],
    'data': [
        #'security/ir.model.access.csv',
        'views/hr_contract_view.xml',

    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
