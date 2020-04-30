{
    'name': 'Employee School Extension',
    'version': '1.1',
    'category': 'Human Resources',
    'sequence': 85,
    'summary': 'Employees School Details',
    'description': """
Human Resources Management
==========================

This application enables you to manage important aspects of your company's staff and other details such as their skills, contacts, working time...


You can manage:
---------------
* Employees and hierarchies : You can define your employee with User and display hierarchies
* HR Departments
* HR Jobs
 """,
    'depends': [],
    'data': [

        'views/employee_school_view.xml',
        'security/ir.model.access.csv',
    ],

    'images': [

        'static/src/img/default_image.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}