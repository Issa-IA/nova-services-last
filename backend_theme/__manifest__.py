# -*- coding: utf-8 -*-

{
    "name": "Theme",
    "description": """ backend theme #343434 for Odoo""",
    "summary": "backend theme #343434 for Odoo",
    "category": "Themes/Backend",
    "version": "15.0.1.0.3",
    'author': 'shayma',
    'company': 'shayma',
    'maintainer': 'shayma',
    'website': "www.company.com",
    "depends": ['base', 'web', 'mail'],
    "data": [
        'views/layout.xml',
    ],
    'assets': {
        'web.assets_frontend': [
        ],
        'web.assets_backend': [
            'backend_theme/static/src/scss/theme_accent.scss',
            'backend_theme/static/src/scss/theme.scss',

        ],
        'web.assets_qweb': [
        ],
    },
    'images': [
    ],
    'license': 'LGPL-3',
    'pre_init_hook': 'test_pre_init_hook',
    'post_init_hook': 'test_post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
