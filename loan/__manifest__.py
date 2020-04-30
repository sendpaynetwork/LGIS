{
    'name': 'Employee Loan',
    'version': '1.1',
    'category': 'Human Resources',
    'sequence': 85,
    'summary': 'Employees Loan Management',
    'description': """
Employee Loan Application Management
==========================

Employee Loan Management


You can manage:
---------------
* Employees and hierarchies : You can define your employee with User and display hierarchies
* HR Departments
* HR Jobs
 """,
    'depends': [],
    'data': [

        'views/loan_view.xml',
        "security/ir.model.access.csv",
    ],

    'images': [

        'static/src/img/default_image.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
