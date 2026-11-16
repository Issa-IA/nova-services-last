# -*- coding: utf-8 -*-
{
    'name': "contactvue",

    'summary': """ """,

    'description': """ """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",


    'category': 'Novatec',
    'version': '18.0.1.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'fleetADD1', 'venteFacturefield'],

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
