from odoo import models, fields, api

class FleetHerit(models.Model):
    _inherit = 'fleet.vehicle'

    partner_id = fields.Many2one('res.partner',ondelete='Set null',string='Contact',index=True)