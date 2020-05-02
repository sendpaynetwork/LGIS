{
    'name':     'COA Tools Integration',
    'version':  '9.0.0.1',
    'author':   'Nigerianet',
    'website':  'http://www.nigerianet.com',
    'summary':  'COA SEGMENT',
    'depends': ['account'],
    'data': [
        #'views/coa_segments_view.xml',
        'views/admin_code_view.xml',
        'views/eco_code_view.xml',
        'views/fun_code_view.xml',
        'views/geo_code_view.xml',
        'views/prog_code_view.xml',
        'views/fund_code_view.xml',
        'views/account_view.xml',
        "security/ir.model.access.csv",

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
