from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class PartnerModelHeritt(models.Model):
    _inherit = 'res.partner'

    partner_parc_ids = fields.One2many('fleet.vehicle', inverse_name='partner_id',string="Matériels")


class SaleOrderLineHerit(models.Model):
    _inherit    = 'sale.order.line'
    price_sale_1 = fields.Monetary(string="Modifier Prix d'achat")
    price_sale = fields.Monetary(string="Prix d'achat", compute="compute_pricesale")
    designation = fields.Char(compute="compute_designation",string="Désignation")
    order_line_serie = fields.Char(string="N° serie",readonly=True)
    
    def _prepare_invoice_line(self,**optional_values):
        res = super(SaleOrderLineHerit, self)._prepare_invoice_line()  
        res.update({'move_line_serie': self.order_line_serie, })
        return res

    @api.depends('name')
    def compute_designation(self):
        for rec in self:
            if rec.name:
                chaine = rec.name.split()
                rec.designation = " ".join(chaine[1:])
            else:
                rec.designation = False

    ####### add new produc
    @api.depends("product_id","price_sale_1")
    def compute_pricesale(self):
        for rec in self:  
            if rec.price_sale_1>0:
                rec.price_sale = rec.price_sale_1
            else:
                rec.price_sale = rec.product_id.standard_price*rec.product_uom_qty






class SaleOrderHerit(models.Model):
    _inherit    = 'sale.order'
    
    #start send email
    sale_expiration_date=fields.Date("Date de fin de contrat",compute='date_expiration_date')
    @api.depends('create_date','sale_periodicite','sale_duree')
    def date_expiration_date(self):
        for rec in self:
            if rec.create_date:
                if rec.sale_periodicite == 'mens':
                    if rec.sale_duree>0:
                        rec.sale_expiration_date = rec.create_date + relativedelta(months=rec.sale_duree)-relativedelta(days=1)
                    else:
                        rec.sale_expiration_date = rec.create_date
                else:
                    rec.sale_expiration_date = rec.create_date

                if rec.sale_periodicite == 'trim':
                    if rec.sale_duree>0:
                        rec.sale_expiration_date = rec.create_date + relativedelta(months=(rec.sale_duree*3)) - relativedelta(days=1)
                    else:
                        rec.sale_expiration_date = rec.create_date
                else:
                    rec.sale_expiration_date = rec.create_date
            else:
                rec.sale_expiration_date = False    
    #end send email
    
    partner_id_new = fields.Many2one('res.partner', 'Client')
    
    @api.onchange("partner_id_new")
    def update_partner_id(self):
        for rec in self:            
            if rec.partner_id_new:
                rec.partner_id = rec.partner_id_new
                rec.street_client = rec.partner_id.street
                rec.zip_client = rec.partner_id.zip
                rec.city_client = rec.partner_id.city
    
    #new montant total de rachat
    sale_total_rachat = fields.Float(string='Montant de rachat total',default=0.0,compute="sale_total_rachat_func")
    @api.onchange("sale_bonretour")
    def sale_total_rachat_func(self):
        for rec in self:
            somme = 0
            if rec.sale_bonretour:
                for retour in rec.sale_bonretour:
                        somme+=retour.bonretour_montant
            rec.sale_total_rachat = somme
    #fin montant de rachat
    
    sale_total_vente = fields.Monetary(string="Total vente",default=0.0,compute="sale_total_vente_func")
    sale_marge  = fields.Monetary(compute="sale_marge_fuc",default=0.0, string="Marge commerciale")
    sale_total_achat = fields.Monetary(string="Total vente", default=0.0, compute="sale_total_achat_func")
    sale_marge_reel = fields.Monetary(default=0.0, string="Marge réelle", compute="sale_marge_reel_fuc")
    sale_date_traitement = fields.Date("Date de traitement",compute="sale_total_date_traitement")
    
    ############ dashboard 
    sale_new_contact = fields.Integer(string="New",default=0)
    @api.onchange("sale_type_client1")
    def rcuperenewcontact(self):
        for rec in self:
            if rec.sale_type_client1 == 'nouveau_client':
                rec.sale_new_contact = 1
    
    #stat dashbooard
    sale_objectif_marge = fields.Float(string="% Marge", compute="sale_objectif_marge_compute",digits=(16, 4))
    
    @api.depends("sale_marge","user_id")
    def sale_objectif_marge_compute(self):
        for rec in self:
            if rec.user_id:
                if rec.user_id.x_studio_marge>0:                      
                    rec.sale_objectif_marge= rec.sale_marge/rec.user_id.x_studio_marge
                else:
                   rec.sale_objectif_marge=0
            else:
                rec.sale_objectif_marge=0
    sale_objectif_marge_stat = fields.Float(string="% Marge", digits=(16, 4), related='sale_objectif_marge',store=False)    
    
    sale_objectif_client = fields.Float(string="% Nombre de clients", compute="sale_objectif_client_compute",digits=(16, 4))
    @api.onchange("sale_new_contact","user_id")
    def sale_objectif_client_compute(self):
        for rec in self:
            if rec.user_id:
                if rec.user_id.x_studio_nombre_de_clients > 0:                
                    rec.sale_objectif_client= rec.sale_new_contact/rec.user_id.x_studio_nombre_de_clients
                else:
                   rec.sale_objectif_client=0 
            else:
                rec.sale_objectif_client=0
    sale_objectif_contrat = fields.Float(string="% Nombre de contrats",compute="sale_objectif_contrat_compute",digits=(16, 4))
    @api.onchange("sale_materiels_vendu","user_id")
    def sale_objectif_contrat_compute(self):
        for rec in self:
            if rec.user_id:
                if rec.user_id.x_studio_nombre_de_contrats > 0:                
                    rec.sale_objectif_contrat= rec.sale_materiels_vendu/rec.user_id.x_studio_nombre_de_contrats
                else:
                   rec.sale_objectif_contrat=0 
            else:
                rec.sale_objectif_contrat=0
    sale_objectif_affaire = fields.Float(string="% Chiffre d'affaire")

    ############ zip street city
    sale_type_client = fields.Selection([('nouveau_client', 'Nouveau client'), ('conversion', 'Conversion'),('additionnel', 'Additionnel')], string='Type de vente')
    sale_type_client1 = fields.Selection([('nouveau_client', 'Nouveau client'), ('conversion', 'Conversion'),
                                         ('additionnel', 'Additionnel')], string='Type de vente')
    sale_materiels_vendu   = fields.Integer(string="MACHINES")    
    street_client = fields.Char(compute="compute_street_client")
    zip_client = fields.Char(compute="compute_zip_client")
    city_client = fields.Char(compute="compute_city_client")
    ############### champs Numéro dossier,
    sale_dossier = fields.Char(string='Dossier N°', compute="rcuperenumerodossier")

    @api.onchange("opportunity_id")
    def rcuperenumerodossier(self):
        for rec in self:
            rec.sale_dossier = rec.opportunity_id.num_dossier
            rec.sale_type_client1 = rec.opportunity_id.action_field


    @api.onchange("partner_id")
    def compute_street_client(self):
        for rec in self:
            if rec.partner_id:
                rec.street_client = rec.partner_id.street
            else:
                rec.street_client = False

    @api.onchange("partner_id")
    def compute_zip_client(self):
        for rec in self:
            if rec.partner_id:
                rec.zip_client = rec.partner_id.zip
            else:
                rec.zip_client = False

    @api.onchange("partner_id")
    def compute_city_client(self):
        for rec in self:
            if rec.partner_id:
                rec.city_client = rec.partner_id.city
            else:
                rec.city_client = False

    
    street_livraison = fields.Char(compute="compute_street_livraison")
    zip_livraison = fields.Char(compute="compute_zip_livraison")
    city_livraison = fields.Char(compute="compute_city_livraison")

    @api.onchange("partner_shipping_id")
    def compute_street_livraison(self):
        for rec in self:
            if rec.partner_shipping_id:
                rec.street_livraison = rec.partner_shipping_id.street
            else:
                rec.street_livraison = False

    @api.onchange("partner_shipping_id")
    def compute_zip_livraison(self):
        for rec in self:
            if rec.partner_shipping_id:
                rec.zip_livraison = rec.partner_shipping_id.zip
            else:
                rec.zip_livraison = False

    @api.onchange("partner_shipping_id")
    def compute_city_livraison(self):
        for rec in self:
            if rec.partner_shipping_id:
                rec.city_livraison = rec.partner_shipping_id.city
            else:
                rec.city_livraison = False

    ##################### fin




    def sale_total_date_traitement(self):
        for rec in self:
            rec.sale_date_traitement =date.today()



    #########  Financement page
    #group 1
    sale_type    = fields.Selection([('location', 'Location'), ('vente', 'Vente')],string='Type',default='location')
    sale_leaser  = fields.Many2one( "typeleaser",string='Leaser')
    sale_finance = fields.Monetary(string="Montant financé")
    sale_frais_restitution = fields.Monetary(string="Frais de restitution",default=0.0)
    sale_frais_restitution_1   = fields.Selection([('nul', "0.00 €"), ('other', "200.00 €")],string='Frais de restitution',default='nul')
    @api.onchange("sale_frais_restitution_1")
    def frais_restitution_update(self):
        for rec in self:
            if rec.sale_frais_restitution_1 == "nul":
                rec.sale_frais_restitution = 0
            if rec.sale_frais_restitution_1 == "other":
                rec.sale_frais_restitution =200
    #group 2
    sale_duree   = fields.Integer(string="Durée")
    sale_accord  = fields.Char(string="N° d'accord")
    sale_loyer   = fields.Monetary(string="Loyer")
    sale_frais_livraison_new   = fields.Monetary(string="Frais de livraison",default=0.0)
    
    sale_frais_livraison_new_1   = fields.Selection([('nul', "0.00 €"), ('other', "250.00 €")],string='Frais de livraison',default='nul')
    @api.onchange("sale_frais_livraison_new_1")
    def frais_livraison_update(self):
        for rec in self:
            if rec.sale_frais_livraison_new_1 == "nul":
                rec.sale_frais_livraison_new =0
            if rec.sale_frais_livraison_new_1 == "other":
                rec.sale_frais_livraison_new =250
    #group 3
    sale_periodicite = fields.Selection([('mens', 'Mensuelle'), ('trim', 'Trimestrielle ')], string='Periodicité')
    sale_reglement   = fields.Selection([('prelevement ', 'Prélevement'), ('mandat', 'Mandat administratif'),('virement', 'Virement '),('cheque', 'Chéque')], string='Mode de reglement')
    sale_frais       = fields.Monetary(string="Frais de livraison")
    sale_collage       = fields.Text(string="Collage")
    #########  Rachats page
    #group 1
    sale_vr_client      = fields.Monetary(string="Montant du rachat")
    sale_ir_prospects   = fields.Monetary(string="Montant du rachat")
    sale_rachat_matriel = fields.Monetary(string="Montant sponsoring")
    sale_montatnt_IR = fields.Monetary(string="Montant des IR")
    sale_date_rachat_prevue = fields.Date("Date de rachat prévue")
    sale_marque_reference = fields.Char(string="Matériels rachetés")
    #groupe 2
    sale_leaser_ra = fields.Many2one( "typeleaser",string='Leaser')
    sale_partenariat = fields.Monetary(string="Montant total de partenariat")
    sale_marque_reference_prospect = fields.Char(string="Matériels rachetés")
    #groupe 3
    sale_accord_rachat = fields.Char(string="Dossier N°")
    sale_solde_2_fois = fields.Monetary(string="Montant solde en 2 fois")
    sale_Gratuite = fields.Monetary(string="Gratuitée copie")
    #groupe 4
    sale_date_fin_F = fields.Date("Date de fin du partenariat")
    sale_date_2_solde = fields.Date("Date de 2éme solde à effectuer")
    # groupe 5 client 2
    sale_vr_client_2 = fields.Monetary(string="Montant du rachat")
    sale_leaser_ra_client_2 = fields.Many2one("typeleaser", string='Leaser')
    sale_accord_rachat_client_2 = fields.Char(string="Dossier N°")
    sale_date_rachat_prevue_client_2 = fields.Date("Date de rachat prévue")
    sale_marque_reference_client_2 = fields.Char(string="Matériels rachetés")



    #########  Maintenance page
    # group 1
    sale_cout_signe_nb = fields.Float(string="Cout copie Signé ",digits=(16, 4))
    sale_cout_actuel_nb = fields.Float(string="Cout copie Actuel ",digits=(16, 4))
    sale_cout_actuel_signe_nb = fields.Float(compute="ecart_actuel_signe_nb",string="Ecart Actuel/Signé",digits=(16, 4))

    @api.onchange("sale_cout_signe_nb","sale_cout_actuel_nb")
    def ecart_actuel_signe_nb(self):
        for rec in self:
            rec.sale_cout_actuel_signe_nb = rec.sale_cout_signe_nb-rec.sale_cout_actuel_nb

    sale_cout_signe_col = fields.Float(string="Coleur: ",digits=(16, 4))
    sale_cout_actuel_col = fields.Float(string="Coleur: ",digits=(16, 4))
    sale_cout_actuel_signe_col = fields.Float(compute="ecart_actuel_signe_col",string="Coleur: ",digits=(16, 4))

    @api.onchange("sale_cout_signe_col", "sale_cout_actuel_col")
    def ecart_actuel_signe_col(self):
        for rec in self:
            rec.sale_cout_actuel_signe_col = rec.sale_cout_signe_col - rec.sale_cout_actuel_col
    # group 2
    sale_forfait_signe_nb = fields.Integer(string="Forfait copie Signé")
    sale_forfait_actuel_nb = fields.Integer(string="Forfait copie Actuel")
    sale_forfait_actuel_signe_nb = fields.Integer(compute="ecart_forfait_actuel_signe_nb",string="Ecart Actuel/Signé")
    sale_char = fields.Char(default="€", readonly=True)


    @api.onchange("sale_forfait_signe_nb", "sale_forfait_actuel_nb")
    def ecart_forfait_actuel_signe_nb(self):
        for rec in self:
            rec.sale_forfait_actuel_signe_nb = rec.sale_forfait_signe_nb - rec.sale_forfait_actuel_nb

    sale_forfait_signe_col = fields.Integer(string="Couleur: ")
    sale_forfait_actuel_col = fields.Integer(string="Couleur: ")
    sale_forfait_actuel_signe_col = fields.Integer(compute="ecart_forfait_actuel_signe_col",string="Couleur: ")

    @api.onchange("sale_forfait_signe_col", "sale_forfait_actuel_col")
    def ecart_forfait_actuel_signe_col(self):
        for rec in self:
            rec.sale_forfait_actuel_signe_col = rec.sale_forfait_signe_col - rec.sale_forfait_actuel_col
    # group 3
    sale_abonnement_service = fields.Monetary(string="Abonnement Service")
    sale_autre_frais        = fields.Monetary(string="Autre frais")

    @api.onchange("sale_frais_livraison_new", "sale_montatnt_IR","sale_total_vente","sale_finance","sale_frais","sale_frais_restitution","sale_vr_client","sale_ir_prospects","sale_vr_client_2","sale_rachat_matriel","sale_Gratuite","sale_partenariat","sale_solde_2_fois")
    def sale_marge_fuc(self):
        for rec in self:
            if rec.sale_maintnance:
                rec.sale_marge = 0
            else:
                rec.sale_marge = rec.sale_finance - rec.sale_frais_livraison_new- rec.sale_total_rachat-rec.sale_montatnt_IR + rec.sale_frais -rec.sale_total_vente- rec.sale_frais_restitution -rec.sale_vr_client-rec.sale_ir_prospects-rec.sale_vr_client_2-rec.sale_rachat_matriel-rec.sale_Gratuite-rec.sale_partenariat-rec.sale_solde_2_fois
            
    @api.onchange("sale_frais_livraison_new","sale_total_rachat","sale_montatnt_IR","sale_total_achat", "sale_finance", "sale_frais", "sale_frais_restitution", "sale_vr_client",
                  "sale_ir_prospects", "sale_vr_client_2", "sale_rachat_matriel", "sale_Gratuite", "sale_partenariat",
                  "sale_solde_2_fois")
    def sale_marge_reel_fuc(self):
        for rec in self:
            if rec.sale_maintnance:
                rec.sale_marge_reel =0
            else:
                rec.sale_marge_reel = rec.sale_finance -rec.sale_frais_livraison_new-rec.sale_total_rachat-rec.sale_montatnt_IR + rec.sale_frais - rec.sale_total_achat - rec.sale_frais_restitution - rec.sale_vr_client - rec.sale_ir_prospects - rec.sale_vr_client_2 - rec.sale_rachat_matriel - rec.sale_Gratuite - rec.sale_partenariat - rec.sale_solde_2_fois

    @api.depends("order_line")
    def sale_total_vente_func(self):
        for rec in self:
            price_total = 0
            if rec.order_line:
                for record in rec.order_line:
                    if record.price_subtotal:
                        price_total+=record.price_subtotal
            rec.sale_total_vente = price_total

    @api.depends("order_line")
    def sale_total_achat_func(self):
        for rec in self:
            marge_reel = 0
            if rec.order_line:
                for record in rec.order_line:
                    if record.price_sale:
                        marge_reel += record.price_sale
            rec.sale_total_achat = marge_reel



    ################### calcul auto pour parc matériels
    sale_parc_ids = fields.One2many('fleet.vehicle', inverse_name='fleet_devis_id',string="Matériels")

    ########## smart button to parc
    par_mat_count = fields.Integer(string="Matériels", compute="compute_mat_count")

    def compute_mat_count(self):
        for rec in self:
            order_count = self.env['fleet.vehicle'].search_count([('fleet_devis_id', '=', rec.id)])
            rec.par_mat_count = order_count

    def action_open_rfq(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Matériels',
            'res_model': 'fleet.vehicle',
            'view_type': 'form',
            'domain': [('fleet_devis_id', '=', self.id)],
            'view_mode': 'kanban,form',
            'target': 'current',

        }

    def createParck(self):
        print("bbbbbbbbbbbbbbb")

        return {
            'type': 'ir.actions.act_window',
            'name': " ",
            'res_model': 'creatpark',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_devis_dossier': self.id},
        }

    sale_notifcation_ok = fields.Boolean(default=False,string="Approbation" )
    def demande_confirmer_devis(self):
        for rec in self:
            if self.env.user.has_group('droits_d_acces.group_Technicien_contact'):
                rec.sale_notifcation_ok = True
    def action_confirm(self):
        res = super(SaleOrderHerit, self).action_confirm()
        if self.partner_id:
            self.partner_id.type_contact = "Client"
        return self.createParck()

    ####################### pop up































