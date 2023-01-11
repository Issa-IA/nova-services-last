# -*- coding: utf-8 -*-
{
    'name': "facturation_automatique",

    'summary': """""",

    'description': """""",

    'author': "My Company",
    'website': "",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
          'security/ir.model.access.csv',
         'views/views.xml',
         'views/parnter_facture.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
