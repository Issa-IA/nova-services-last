# -*- coding: utf-8 -*-
{
    'name': "custom invoice report",

    'summary': """ """,

    'description': """ """,

    'author': "IssaIA",
    'website': " ",

    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account'],

    # always loaded
    'data': [

        'views/invoice_report.xml',
        'views/ir_actions_report.xml',

    ],
    # only loaded in demonstration mode

}
