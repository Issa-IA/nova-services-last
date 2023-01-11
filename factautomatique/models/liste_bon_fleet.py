from odoo import models, fields, api


class listbonfleet(models.Model):
    _name = 'listboncommandefleet'
    name = fields.Char(string='Bon de commande et matériels')
    fleet_id = fields.Many2one('fleet.vehicle', string='les numéros de série')
    devis_id = fields.Many2one('sale.order', string='Devis')
    comp_couleur_diff = fields.Integer(string="Nombre de pages couleur à facturer")
    comp_noir_diff = fields.Integer(string="Nombre de pages noir à facturer")





