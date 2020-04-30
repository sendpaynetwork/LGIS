{
    'name':     'Tools Integration',
    'version':  '9.0.0.1',
    'author':   'Nigerianet',
    'website':  'http://www.nigerianet.com',
    'summary':  'MDA',
    'description': """
MDA Information
===================================================

This application enables you to view MDA record...


You can manage:
---------------
* Employee MDA

    """,
    'depends': [],
    'data': [

        'views/mda_view.xml',
        "security/ir.model.access.csv",

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
