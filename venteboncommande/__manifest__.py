# -*- coding: utf-8 -*-
{
    'name': "venteboncommande",

    'summary': """
    Create sale order from sale order
    """,

    'description': """
    Create sale order from sale order
    """,

    'category': 'Novatec',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'venteADD1', 'fleet'],

    # always loaded
    'data': [
        'data/actions.xml',
        'data/menu.xml',
    ],
}
