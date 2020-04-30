{
    'name':     'TSA Rate',
    'version':  '9.0.0.1',
    'author':   'Nigerianet',
    'website':  'http://www.nigerianet.com',
    'summary':  'TSA Tool',
    'description': """
Subeb Employee Paypoint Configuration
===============================================

This application enables you to view and configure tsa for staff


You can view:
---------------
* Paypoint

    """,
    'depends': ['hr'],
    'data': [

        'views/tsa_view.xml',
        "security/ir.model.access.csv",

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
