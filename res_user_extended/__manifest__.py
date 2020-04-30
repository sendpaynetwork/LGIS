{
    'name': 'User Extension',
    'version': '1.1',
    'category': 'User Resources',
    'sequence': 85,
    'summary': 'User Bank Details',
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
    'depends': ['resource', 'hr_contract', 'employee_school'],
    'data': [
        'views/res_users.xml',
    ],

    'images': [

        'static/src/img/default_image.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}