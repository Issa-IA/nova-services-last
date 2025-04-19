# -*- coding: utf-8 -*-
{
    'name': "view updgrade v18",

    'summary': """ """,

    'description': """ """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','fleet', 'crm','sale', 'helpdesk', 'stock'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/helpdesk_inherit_v18_view.xml',
        'views/sale_view_v18_inherit.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
