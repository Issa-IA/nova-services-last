from odoo import _, api, fields, models


    

class   Crmteamoinhertit(models.Model):
    _inherit = "crm.team"

    crm_team_comer = fields.Monetary("Marge")
    crm_team_chif = fields.Monetary("Chiffre d'affaire")
    crm_team_N_client = fields.Integer("Nombre de clients")
    crm_team_N_contrat= fields.Integer("Nombre de contrats")
    
        
    @api.onchange("member_ids")
    def equipe_ob_total(self):
        for rec in self:  
                team_comer = 0
                team_chif  = 0
                team_N_client = 0
                team_N_contrat = 0
                for user in rec.member_ids:
                    team_N_contrat+=user.x_studio_nombre_de_contrats
                    team_N_client+=user.x_studio_nombre_de_clients
                    team_chif+= user.x_studio_chiffre_daffaire
                    team_comer+=user.x_studio_marge
                rec.crm_team_comer = team_comer
                rec.crm_team_chif = team_chif
                rec.crm_team_N_client = team_N_client
                rec.crm_team_N_contrat = team_N_contrat


class SaleOrderHeritcomerce(models.Model):
    _inherit    = 'sale.order'

    ########## objectif_total_equipe comerciale
    sale_N_contrat = fields.Float(string="%Nombre de contrats total")

    @api.onchange("sale_new_contrat","order_line")
    def equipe_comercial_contrat(self):
        for rec in self:
            team_vente = False
            for record in rec.user_id.crm_team_ids:
                id = 1
                if record.id == 1:
                    team_vente = record
            if team_vente:
                if len(rec.order_line) > 0 and team_vente.crm_team_N_contrat > 0:
                    rec.sale_N_contrat = rec.sale_new_contrat / team_vente.crm_team_N_contrat / len(rec.order_line)
                    print("Nombre de clients total",
                          rec.sale_new_contact / team_vente.crm_team_N_contrat / len(rec.order_line))
    
    sale_contrat_tot = fields.Float(string="%Nbre contrats tot")
    @api.onchange("sale_new_contrat","order_line")
    def equipe_comercial_contrat_t(self):
        for rec in self:
            team_vente = False
            for record in rec.user_id.crm_team_ids:
                id = 1
                if record.id == 1:
                    team_vente = record
            if team_vente:
                if len(rec.order_line) > 0 and team_vente.crm_team_N_contrat > 0:
                    rec.sale_contrat_tot = rec.sale_new_contrat / team_vente.crm_team_N_contrat / len(rec.order_line)
                    print("Nombre de clients total",
                          rec.sale_new_contact / team_vente.crm_team_N_contrat / len(rec.order_line))
     

    sale_N_client = fields.Float(string="%Nombre de clients total")
    @api.onchange("sale_new_contact","order_line")
    def equipe_comercial_client(self):
        for rec in self:
            team_vente = False
            for record in rec.user_id.crm_team_ids:
                id = 1
                if record.id == 1:
                    team_vente = record
            if team_vente:
                if len(rec.order_line) > 0 and team_vente.crm_team_N_client > 0:
                    rec.sale_N_client = rec.sale_new_contact / team_vente.crm_team_N_client / len(rec.order_line)
                    print("Nombre de clients total", rec.sale_new_contact / team_vente.crm_team_N_client / len(rec.order_line))

    sale_client_tot = fields.Float(string="%Nbre clients tot")
    @api.onchange("sale_new_contact","order_line")
    def equipe_comercial_client_t(self):
        for rec in self:
            team_vente = False
            for record in rec.user_id.crm_team_ids:
                id = 1
                if record.id == 1:
                    team_vente = record
            if team_vente:
                if len(rec.order_line) > 0 and team_vente.crm_team_N_client > 0:
                    rec.sale_client_tot = rec.sale_new_contact / team_vente.crm_team_N_client / len(rec.order_line)
                    print("Nombre de clients total", rec.sale_new_contact / team_vente.crm_team_N_client / len(rec.order_line))
                    
    sale_comer = fields.Float(string="%Marge comercial total")
    @api.onchange("x_studio_marge_commerciale","order_line")
    def equipe_comercial_marge(self):
        for rec in self:
            team_vente = False
            for record in rec.user_id.crm_team_ids:
                id = 1
                if record.id == 1:
                    team_vente = record
            if team_vente:
                if len(rec.order_line) > 0 and team_vente.crm_team_comer > 0:
                    rec.sale_comer = rec.x_studio_marge_commerciale / team_vente.crm_team_comer / len(rec.order_line)
                    print("Marge comercial", rec.x_studio_marge_commerciale / team_vente.crm_team_comer / len(rec.order_line))

    sale_chifre_aff = fields.Float(string="%Chiffre d'affaire total")
    @api.onchange("sale_finance","order_line")
    def equipe_comercial_chifre(self):
        for rec in self:
            team_vente = False
            for record in rec.user_id.crm_team_ids:
                id = 1
                if  record.id == 1:
                    team_vente = record
            if team_vente:
                if len(rec.order_line)>0 and team_vente.crm_team_chif>0:
                    rec.sale_chifre_aff = rec.sale_finance/team_vente.crm_team_chif/len(rec.order_line)
                    print("Chiffre d'affaire", rec.sale_finance/team_vente.crm_team_chif/len(rec.order_line))

    ########## fin total_equipe comerciale
    sale_contrat_tot_new = fields.Float(string="%Nbre contrats tot new")
    @api.onchange("sale_new_contrat")
    def equipe_comercial_contrat_new(self):
        for rec in self:
            team_vente = False
            for record in rec.user_id.crm_team_ids:
                id = 1
                if record.id == 1:
                    team_vente = record
            if team_vente:
                if team_vente.crm_team_N_contrat > 0:
                    rec.sale_contrat_tot_new = rec.sale_new_contrat / team_vente.crm_team_N_contrat 
    
    sale_client_tot_new = fields.Float(string="%Nbre clients tot new")
    @api.onchange("sale_new_contact")
    def equipe_comercial_client_new(self):
        for rec in self:
            team_vente = False
            for record in rec.user_id.crm_team_ids:
                id = 1
                if record.id == 1:
                    team_vente = record
            if team_vente:
                if team_vente.crm_team_N_client > 0:
                    rec.sale_client_tot_new = rec.sale_new_contact / team_vente.crm_team_N_client
    ###
    sale_comer_new = fields.Float(string="%Marge comercial tot new")
    @api.onchange("x_studio_marge_commerciale")
    def equipe_comercial_marge_new(self):
        for rec in self:
            team_vente = False
            for record in rec.user_id.crm_team_ids:
                id = 1
                if record.id == 1:
                    team_vente = record
            if team_vente:
                if  team_vente.crm_team_comer > 0:
                    rec.sale_comer_new = rec.x_studio_marge_commerciale / team_vente.crm_team_comer 
    
    sale_chifre_aff_new = fields.Float(string="%Chiffre d'affaire tot new")
    @api.onchange("sale_finance")
    def equipe_comercial_chifre_new(self):
        for rec in self:
            team_vente = False
            for record in rec.user_id.crm_team_ids:
                id = 1
                if  record.id == 1:
                    team_vente = record
            if team_vente:
                if team_vente.crm_team_chif>0:
                    rec.sale_chifre_aff_new = rec.sale_finance/team_vente.crm_team_chif



















