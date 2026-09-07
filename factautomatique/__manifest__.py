# -*- coding: utf-8 -*-
{
    'name': "facturation_automatique",

    'summary': """""",

    'description': """""",

    'author': "My Company",
    'website': "",


    'category': 'Novatec',
    'version': '18.0.1.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'fleet'],

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
       'post_init_hook': '_backfill_fact_date_derniere_facturation',
}
