"""Hooks for Changing Menu Web_icon"""
# -*- coding: utf-8 -*-

import base64

from odoo import api, SUPERUSER_ID
from odoo.modules import get_module_resource


def test_pre_init_hook(cr):
    """pre init hook"""

    env = api.Environment(cr, SUPERUSER_ID, {})
    menu_item = env['ir.ui.menu'].search([('parent_id', '=', False)])




def test_post_init_hook(cr, registry):
    """post init hook"""

    env = api.Environment(cr, SUPERUSER_ID, {})
    menu_item = env['ir.ui.menu'].search([('parent_id', '=', False)])
