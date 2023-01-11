from odoo import models, fields, api


class HelpdeskModelHerit(models.Model):
    _inherit = 'helpdesk.ticket'

  
    product_serie_id = fields.Many2one('fleetserielarticle', string='Article',domain="[('client_id', '=', partner_id)]")

