# -*- coding: utf-8 -*-
{
    'name': "crm team objectif",

    'summary': """ """,

    'description': """ """,

    'author': "IssaIA",
    'website': " ",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','crm','contacts'],

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
