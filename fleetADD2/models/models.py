from odoo import models, fields, api

#add field periodicité
class FleetSErieInherit(models.Model):
    _inherit = 'fleet.vehicle'

    def write(self, vals):
        res = super(FleetSErieInherit, self).write(vals)
        for rec in self:
            list_fleet_active = [ a['fleet_id'][0] for a in self.env['fleetserielarticle'].search_read([('fleet_id', '=', rec.id)],['fleet_id'])]

            if list_fleet_active !=[]:
                record = self.env['fleetserielarticle'].search([('id', '=', list_fleet_active[0])])
                record.update({
                    'num_serie': rec.fleet_serie,
                    'client_id': rec.partner_id.id,
                    'fleet_id': rec.id,
                    'article_id': rec.fleet_artic_id.id,
                          })

            else:
                vals = {
                    'num_serie': rec.fleet_serie,
                    'client_id': rec.partner_id.id,
                    'fleet_id': rec.id,
                    'article_id': rec.fleet_artic_id.id,
                }
                self.env['fleetserielarticle'].create(vals)

        return res

class clientfleetserielarticle(models.Model):
    _name = 'fleetserielarticle'
    _description = ' client fleet seriel article'
    num_serie = fields.Char(string='Numéros de série',related='fleet_id.fleet_serie')
    client_id = fields.Many2one('res.partner', ondelete='Set null', string='Client', index=True)
    fleet_id = fields.Many2one('fleet.vehicle', string='Par Matériel')
    article_id = fields.Many2one('product.product', string='Matériel')

    @api.onchange('fleet_id')
    def num_serie_upadte(self):
        if self.fleet_id:
            self.num_serie = self.fleet_id.fleet_serie
            self.client_id = self.fleet_id.partner_id.id
            self.article_id = self.fleet_id.fleet_artic_id.id


    def name_get(self):
        result = []
        for model in self:
            if model.fleet_id:
                name = model.fleet_id.name_get()[0][1]

            else:
                name = "Pas de Parc"
            result.append((model.id, name))
        return result

