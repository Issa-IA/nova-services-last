# -*- coding: utf-8 -*-
{
    'name': "view updgrade v18",

    'summary': """ """,

    'description': """ """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",


    'category': 'Novatec',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','fleet', 'crm','sale', 'helpdesk', 'stock'],

    # always loaded
    'data': [
        'views/helpdesk_inherit_v18_view.xml',
        'views/sale_view_v18_inherit.xml'
    ],
}
