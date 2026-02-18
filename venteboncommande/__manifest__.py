# -*- coding: utf-8 -*-
{
    'name': "venteboncommande",

    'summary': """
    Create sale order from sale order
    """,

    'description': """
    Create sale order from sale order
    """,

    'category': 'Sales',
    'version': '18.0.0.0.3',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'venteADD1', 'fleet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'data/actions.xml',
        'data/menu.xml',
    ],
}
