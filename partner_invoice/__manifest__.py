# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Partner_invoice',
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
    ],
    'data': [
        'view/partner_invoice.xml',
        'view/groupe_commercial_access.xml',
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
