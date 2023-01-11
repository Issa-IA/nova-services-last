# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'CRM',
    'version': '1.6',
    'category': 'Sales/CRM',
    'sequence': 15,
    'summary': 'Track leads and close opportunities',
    'description': "",
    'website': 'https://www.odoo.com/app/crm',
    'depends': [
        'base_setup',
        'sale_management',
        'uom',
        'base',
        'crm',
        'contacts',
        'fleet',
    ],
    'data': [
        'view/inherit_view_crm.xml',
        'view/inherit_view_fleet.xml',
        'data/ir_sequence_data.xml',
        'view/partner_view_inherit.xml',
    ],
    'demo': [
    ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,
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
