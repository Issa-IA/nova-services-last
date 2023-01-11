# -*- coding: utf-8 -*-
{
    'name': "ReadingExcel",

    'summary': """ """,

    'description': """ """,

    'author': "My Company",
    'website': " ",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet','sale'],
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
