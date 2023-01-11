from odoo import models, fields, api


class   Contactinhertit(models.Model):
    _inherit = "res.partner"
    
    ############################# facturation mail    
    def get_mail(self):
        for rec in self:
            if rec.courriel_facturation:
                rec.courriel_facturation_reel = rec.courriel_facturation
            else:
                rec.courriel_facturation_reel = rec.email

    courriel_facturation = fields.Char(string='Courriel de facturation')
    courriel_facturation_reel = fields.Char(string='Courriel de facturation', compute="get_mail", store=False, readonly=False)

    @api.onchange("courriel_facturation", "email")
    def recuperecourriel_facturation(self):
        for rec in self:
            if rec.courriel_facturation:
                rec.courriel_facturation_reel = rec.courriel_facturation
            else:
                rec.courriel_facturation_reel = rec.email
    ########################

    par_count = fields.Integer(string="Factures", compute="compute_mat_count")

    def compute_mat_count(self):
        for rec in self:
            fact_count = self.env['account.move'].search_count(
                [('partner_id', '=', rec.id), ('acount_maintnance', '=', 'True')])
            rec.par_count = fact_count

    def open_action_fact(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Factures maintenances',
            'res_model': 'account.move',
            'view_type': 'form',
            'domain': [('partner_id', '=', self.id), ('acount_maintnance', '=', 'True')],
            'view_mode': 'tree,form',
            'target': 'current',

        }

    parc_count = fields.Integer(string="Matériels", compute="compute_parc_count")

    def compute_parc_count(self):
        for record in self:
            parc_= self.env['fleet.vehicle'].search_count([('partner_id', '=', record.id)])
            record.parc_count = parc_

    def open_action_parc(self):
        return {

            'type': 'ir.actions.act_window',
            'name': 'Matériels',
            'res_model': 'fleet.vehicle',
            'view_type': 'form',
            'domain': [('partner_id', '=', self.id)],
            'view_mode': 'kanban,form',
            'target': 'current',

        }







