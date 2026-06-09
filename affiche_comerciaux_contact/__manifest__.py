# -*- coding: utf-8 -*-
{
    'name': "Contacts pour commerciaux",

    'summary': """ """,

    'description': """ """,

    'author': "My Company",
    'website': " ",


    'category': 'Novatec',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
