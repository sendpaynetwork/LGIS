{
    'name':     'Pay Point',
    'version':  '9.0.0.1',
    'author':   'Nigerianet',
    'website':  'http://www.nigerianet.com',
    'summary':  'Paypoint Tool',
    'depends': ['mda'],
    'data': [

        'views/emp_pay_view.xml',
        "security/ir.model.access.csv",

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
