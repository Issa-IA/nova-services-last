from odoo import models, fields, api
from datetime import date
import math
from dateutil.relativedelta import relativedelta

############### new model
class typformat(models.Model):
    _name        = 'typformat'
    _description = 'Type Info infos MATERIELS'
    name         = fields.Char(string='Format')
    def name_get(self):
        result = []
        for model in self:
            name = model.name
            result.append((model.id, name))
        return result
############


class fleetNameGET(models.Model):
    _inherit = 'fleet.vehicle.model'
    type_materiels = fields.Selection([('print', 'Print'), ('sauvegarde', 'Sauvegarde'), ('solution', 'Solution'), ('ecran', 'Ecran')],string='Type de matériel')
    model_format1 = fields.Many2one('typformat',string='Format')
    model_format = fields.Selection([('a3', 'A3'), ('a2', 'A4')], string='Format')
    model_attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='Pièces jointes')

    def name_get(self):
        result = []
        for model in self:
            name = model.name
            result.append((model.id, name))
        return result


class TypeInfo(models.Model):
    _name        = 'typeinfo'
    _description = 'Type Info infos MATERIELS'
    name         = fields.Char('Type')

class TypeLeaser(models.Model):
    _name        = 'typeleaser'
    _description = 'Type de leaser infos CONTRATS'
    name         = fields.Char('Leaser')

#add field periodicité
class FleetContINHERIT(models.Model):
    _inherit = 'fleet.vehicle'
    fleet_type_materiel=  fields.Char(string="Type de matériel")
    fleet_type_materiels_fin = fields.Selection([('print', 'Print'), ('sauvegarde', 'Sauvegarde'), ('solution', 'Solution'), ('ecran', 'Ecran')],string='Type de matériel', related="fleet_Modele.type_materiels")
    image_materiel  = fields.Binary()
    model_id = fields.Many2one(required=False )
    fleet_dossier_devis = fields.Char(string='Dossier N°')
    # rendre the default = actif
    state_id = fields.Many2one(default=1)
    ####facture
    comp_couleur_depart = fields.Integer(string="Compteur de départ Couleur", default='0')
    comp_noir_depart = fields.Integer(string="Compteur de départ NB", default='0')

    compt_depart_ok = fields.Boolean(default=False)


    ###############
    #   Contrat  #
    #############
    fleet_periodicite = fields.Selection([('mens', 'Mensuelle'), ('trim', 'Trimestrielle')],string='Periodicité')
    fleet_date_inst   = fields.Date("Date d'installation",default=date.today())
    fleet_expiration_date = fields.Date("Date de fin de contrat")
    fleet_duree       = fields.Integer("Durée de contrat")
    fleet_duree_rest  = fields.Integer("Durée restante",compute='duree_rest',store=True)
    fleet_prix_HT     = fields.Monetary("Prix HT")
    fleet_solde_est   = fields.Monetary("Solde estimatif",compute='solde_estimatif')
    fleet_type = fields.Selection([('location', 'Location'), ('vente', 'Vente')],string='Type de vente',default='location')
    fleet_leaser = fields.Many2one( "typeleaser",string='Leaser')
    fleet_accord = fields.Char(string="N° d'accord")

    fleet_trimestre_help = fields.Char(string="help ", compute="trimestre_help")
    fleet_trimestre_help1 = fields.Char(string="help 1", compute="trimestre_help1")

    @api.depends('fleet_periodicite','fleet_duree')
    def trimestre_help(self):
        for rec in self:
            if rec.fleet_periodicite =='trim':
                if rec.fleet_duree > 1:
                    rec.fleet_trimestre_help = "Trimestres"
                else:
                    rec.fleet_trimestre_help = "Trimestre"
            elif rec.fleet_periodicite =='mens':
                rec.fleet_trimestre_help = "Mois"
            else:
                rec.fleet_trimestre_help = " "
    @api.depends('fleet_periodicite','fleet_duree_rest')
    def trimestre_help1(self):
        for rec in self:
            if rec.fleet_periodicite =='trim':
                if rec.fleet_duree_rest > 1:
                    rec.fleet_trimestre_help1 = "Trimestres"
                else:
                    rec.fleet_trimestre_help1 = "Trimestre"

            elif rec.fleet_periodicite =='mens':
                rec.fleet_trimestre_help1 = "Mois"
            else:
                rec.fleet_trimestre_help1 = " "

    @api.depends('fleet_prix_HT','fleet_duree_rest')
    def solde_estimatif(self):
        for rec in self:
            rec.fleet_solde_est = rec.fleet_prix_HT*rec.fleet_duree_rest

    @api.depends('fleet_expiration_date','fleet_date_inst', 'fleet_duree', 'fleet_periodicite', 'fleet_expiration_date')
    def duree_rest(self):
        for rec in self:
            if rec.fleet_expiration_date:
                if rec.fleet_expiration_date > date.today():
                    if rec.fleet_periodicite == 'mens':
                        date1 = date.today()-relativedelta(days=1)
                        date2 = rec.fleet_expiration_date
                        num_months = (date2.year - date1.year) * 12 + (date2.month - date1.month)
                        if num_months>1:
                            rec.fleet_duree_rest = num_months-1
                        else:
                            rec.fleet_duree_rest = 0
                    elif rec.fleet_periodicite == 'trim':
                        date1 = date.today() - relativedelta(days=1)
                        date2 = rec.fleet_expiration_date
                        num_months = (date2.year - date1.year) * 12 + (date2.month - date1.month)
                        rec.fleet_duree_rest = math.floor(num_months/3)
                    else:
                        rec.fleet_duree_rest = 0
                else:
                    rec.fleet_duree_rest = 0
            else:
                rec.fleet_duree_rest = 0

    @api.onchange('fleet_date_inst', 'fleet_duree', 'fleet_periodicite')
    @api.depends('fleet_date_inst','fleet_duree','fleet_periodicite')
    def fleet_date_fin(self):
        for rec in self:
            if rec.fleet_date_inst:
                if rec.fleet_periodicite == 'mens':
                    if rec.fleet_duree>0:
                        rec.fleet_expiration_date = rec.fleet_date_inst + relativedelta(months=rec.fleet_duree)-relativedelta(days=1)
                    else:
                        rec.fleet_expiration_date = rec.fleet_date_inst

                if rec.fleet_periodicite == 'trim':
                    if rec.fleet_duree>0:
                        rec.fleet_expiration_date = rec.fleet_date_inst + relativedelta(months=(rec.fleet_duree*3)) - relativedelta(days=1)
                    else:
                        rec.fleet_expiration_date = rec.fleet_date_inst


    ####################
    #  infos MATÉRIELS #
    ####################
    partner_id = fields.Many2one('res.partner', ondelete='Set null', string='Client', index=True)
    fleet_user_id = fields.Many2one('res.users',  string='Commercial',default=lambda self: self.env.user)
    
    ##############################
    fleet_serie = fields.Char(string="N° serie")
    fleet_fournisseur = fields.Many2one('res.partner', ondelete='Set null',string="Fournisseur",index=True)
    fleet_marque = fields.Many2one( "fleet.vehicle.model.brand",string='Marque',related="fleet_Modele.brand_id")
    fleet_Modele = fields.Many2one( "fleet.vehicle.model",string='Modèle')
    fleet_equipement = fields.Char(string="Équipement")
    fleet_type_1 = fields.Char(string='Type', compute="fleet_type_compute")
    fleet_installation = fields.Char(string="Lieu d'installation")
    fleet_commentaires = fields.Text(string="Commentaires")
    @api.onchange('fleet_Modele')
    def fleet_type_compute(self):
        for rec in self:
            if rec.fleet_Modele.category_id:
                if rec.fleet_Modele.model_format1:
                    rec.fleet_type_1 = str(rec.fleet_Modele.category_id.name) + ' ' + str(rec.fleet_Modele.model_format1.name)
                else:
                    rec.fleet_type_1 = str(rec.fleet_Modele.category_id.name)
            else:
                rec.fleet_type_1 = False


    ######################
    #  infos MAINTENANCE #
    ###################### Mensuelle
    fleet_facturation = fields.Selection([('mens', 'MENSUELLE'), ('trim', 'TRIMESTRIELLE')], string='Facturation')
    @api.onchange('fleet_periodicite')
    def facturationType(self):
        for rec in self:
            if rec.fleet_periodicite == 'trim':
                rec.fleet_facturation = 'trim'
            if rec.fleet_periodicite == 'mens':
                rec.fleet_facturation = 'mens'

    fleet_debut_contrat_date = fields.Date("Date de début de contrat")

    fleet_cout_Couleur = fields.Float(string="Cout copie COULEUR",digits=(16, 4))
    fleet_forfait_couleur = fields.Integer(string="Forfait COULEUR")
    fleet_cout_nb = fields.Float(string="Cout copie NB",digits=(16, 4))
    fleet_forfait_nb = fields.Integer(string="Forfait NB")
    fleet_abonnement_service = fields.Monetary(string="Abonnement Service")
    fleet_autre = fields.Monetary(string="Autre")
                             ############# help Unit
    fleet_unit_HT_Copie = fields.Char(string="help 1", compute="HT_Copie")
    def HT_Copie(self):
        for rec in self:
            rec.fleet_unit_HT_Copie="€ HT/Copie"
    fleet_unit_Copie = fields.Char(string="help 1", compute="Copie_unit")
    def Copie_unit(self):
        for rec in self:
            rec.fleet_unit_Copie ="Copies"

    ######################
    #  infos FINANCIERES #
    ######################
    fleet_partenariat = fields.Monetary(string="Partenariat")
    fleet_date_fin_F = fields.Date("Date de fin")
    fleet_solde_fois = fields.Monetary(string="Solde en 2 fois(1er solde)")
    fleet_date_2_solde = fields.Date("Date de 2éme solde à faire")
    fleet_solde_Montant = fields.Monetary(string="Montant de 2éme solde")




   ############
    #  Vehicle #
    ############
    


    def name_get(self):
        result = []
        for model in self:
            if model.fleet_marque:
                if model.fleet_Modele:
                    if model.fleet_serie:
                        name = model.fleet_marque.name +'/'+ model.fleet_Modele.name+'(' + model.fleet_serie + ')'
                    else:
                        name = model.fleet_marque.name +'/'+ model.fleet_Modele.name+'(' + "Pas de N° serie" + ')'
                else:
                    name = model.fleet_marque.name
            else:
                name = "Pas de matériel"

            result.append((model.id, name))
        return result
    ## infos pour le calcul automatique
    fleet_artic_id = fields.Many2one('product.product', string='Matériel')
    fleet_devis_id = fields.Many2one('sale.order', string='Devis')
    
    @api.onchange('fleet_Modele', 'fleet_marque')
    def ajouter_article(self):
        if self.fleet_marque.id:
            result = self.env['product.product'].search(
                [('product_marque', '=', self.fleet_marque.id), ('product_Modele', '=', self.fleet_Modele.id)])
            for record in self:
                if result:
                    record.fleet_artic_id = result[0]


    
























