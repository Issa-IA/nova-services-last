# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'helpdesk_inherit',
    'version': '1.6',
    'category': 'After-Sales',
    'sequence': 15,
    'summary': 'Helpdesk',
    'description': "",
    'website': 'https://www.odoo.com/app/crm',
    'depends': [
        'base_setup',
        'uom',
        'base',
        'helpdesk',
    ],
    'data': [
        'view/hepdesk_inherit_view.xml',

    ],
    'demo': [
    ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'assets': {
        'web.assets_qweb': [

        ],
        'web.assets_backend': [

        ],
        'web.assets_tests': [

        ],
        'web.qunit_suite_tests': [

        ],
    },
    'license': 'LGPL-3',
}
