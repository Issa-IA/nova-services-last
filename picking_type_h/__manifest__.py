# -*- coding: utf-8 -*-
{
    'name': "picking type inherit",

    'summary': """ """,

    'description': """ """,

    'author': "IssaIA",
    'website': " ",

    'category': 'Novatec',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
