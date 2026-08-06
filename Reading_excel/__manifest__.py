# -*- coding: utf-8 -*-
{
    'name': "ReadingExcel",

    'summary': """ """,

    'description': """ """,

    'author': "My Company",
    'website': " ",

    'category': 'Novatec',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet','sale','product', 'sale','contacts', 'fleetADD1'],
    #'external_dependencies': {'python': ['StringIO'],},

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/compteurColeur.xml',
        'views/copteurNoir.xml',
        'views/vehicule_inherit.xml',
        'views/volume_moy_compteur.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
