{
    'name': 'Employee Update',
    'version': '1.1',
    'category': 'Human Resources',
    'sequence': 85,
    'summary': 'Employees Details Update',
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
    'depends': ['hr','hr_payroll','grade_step'],
    #'depends': ['base_setup', 'mail', 'resource','web_kanban','web_tip'],
    'data': [

        'views/hr_employee_update.xml',
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