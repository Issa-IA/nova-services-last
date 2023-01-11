# -*- coding: utf-8 -*-
{
    'name': "venteADD2",

    'summary': """""",

    'description': """""",

    'author': "",
    'website': "",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/listofserielnumber1.xml',
        'views/sale_order_inherit_button.xml',
        'views/serielnumberfin.xml',
        #'views/stockproductlotinherit.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
