from odoo import models, fields, api

class CrmHerit(models.Model):
    _inherit = 'crm.lead'

    action_field = fields.Selection([('nouveau_client', 'Nouveau client'), ('additionnel', 'Additionnel'),
                                               ('conversion', 'Conversion')], default ='nouveau_client', string="Type de vente")
    materiels = fields.Char('Matériels')
    num_dossier = fields.Char('Numéro de dossier', readonly=True)
    date_signature_prevue = fields.Date('Date de signature prêvue')
    attachment_ids = fields.Many2many( comodel_name='ir.attachment',string='Pièces jointes')

    @api.model
    def create(self, vals):
        record = super(CrmHerit, self).create(vals)
        record['num_dossier'] = self.env['ir.sequence'].next_by_code('crm.num')
        return record



