{
    'name': 'Employee Union',
    'version': '1.1',
    'category': 'Human Resources',
    'sequence': 85,
    'summary': 'Employees Union Details',
    'description': """
Employee Union Management
==========================

This application enables you to manage important aspects of your company's staff and other details such as their skills, contacts, working time...


You can manage:
---------------
* Employees and hierarchies : You can define your employee with User and display hierarchies
* HR Departments
* HR Jobs
 """,
    'depends': [
                ],
    'data': [

        'views/emp_union_view.xml',
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
