# -*- coding: utf-8 -*-
{
    'name': "venteADD1",

    'summary': """  """,

    'description': """ """,

    'author': "",
    'website': "",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','contacts','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_line.xml',
        'views/partner.xml',
        'views/product_inherit.xml',
        'views/serach_advanced_partner.xml',
        'views/serach_advanced_partner_add.xml',
        'views/bonretour.xml',
        'views/stock_inherit.xml',
        #'views/goup_commercial.xml',
        'wizard/create_park.xml',
        'security/security.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
