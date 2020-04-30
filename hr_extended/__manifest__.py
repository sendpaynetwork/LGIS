{
    'name': 'Employee Extension',
    'version': '1.1',
    'category': 'Human Resources',
    'sequence': 85,
    'summary': 'Employees Details',
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

        'views/hr_view.xml',
        'views/hr_views_menu.xml',
        'views/res_bank_views.xml',
        # 'report/report_employee1.xml',
        # 'views/report_hr_employee.xml',
        'security/ir.model.access.csv',
        'security/hr_security.xml',
    ],

    'images': [

        'static/src/img/default_image.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}