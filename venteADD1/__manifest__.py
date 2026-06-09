# -*- coding: utf-8 -*-
{
    'name': "venteADD1",
    'summary': """  """,
    'description': """ """,
    'category': 'Novatec',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'crm', 'contacts', 'product', 'fleet', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_line.xml',
        'views/product_inherit.xml',
        'views/serach_advanced_partner.xml',
        'views/serach_advanced_partner_add.xml',
        'views/bonretour.xml',
        'views/stock_inherit.xml',
        'wizard/create_park.xml',
        'security/security.xml',
    ],
}
