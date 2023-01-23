from odoo import _, api, fields, models
from datetime import date,datetime

from dateutil.relativedelta import relativedelta

class   Anneemodel(models.Model):
    _name = "anneevente"
    _description = 'stat par an'
    annee = fields.Integer("Année",default=2023, required=True)
    annee_team = fields.Many2one( "crm.team",string='Équipe commerciale', required=True)
    mois = fields.One2many('moisvente', inverse_name='annee',string="Mois")
    annee_chifre_ob = fields.Float(string="Obj CA", compute="update_anneee")
    annee_chifre_aff = fields.Float(string="%")
    annee_comer_ob = fields.Float(string="Obj MC")   
    annee_comer = fields.Float(string="%")   
    annee_reel_ob = fields.Float(string="Obj MR")
    annee_reel = fields.Float(string="%")
    annee_livraison_ob = fields.Float(string="Obj FL")
    annee_livraison = fields.Float(string="%")
    anee_contrat_ob = fields.Float(string="Obj NB CONTRAT")
    anee_contrat = fields.Float(string="%")
    annee_client_ob = fields.Float(string="Obj NEW")
    annee_client = fields.Float(string="%")
    annee_materiels_ob = fields.Float(string="Obj NB MATERIELS")
    annee_materiels = fields.Float(string="%")
    
    @api.depends('mois')
    def update_anneee(self):
                for rec in self:
                    chiff_obj = 0
                    chiff     = 0   
                    marge_obj    = 0
                    marge     = 0
                    contrat_obj   = 0
                    contrat   = 0
                    client_obj    = 0
                    client    = 0
                    reel_obj      = 0 
                    reel      = 0 
                    livraison_obj = 0
                    livraison = 0
                    mat = 0
                    mat_obj = 0
                    for ligne in rec.mois:
                        chiff_obj += ligne.moi_chifre_aff_ob
                        chiff     += ligne.moi_chifre_aff
                        marge_obj    +=ligne.moi_comer_ob
                        marge     += ligne.moi_comer
                        contrat_obj   += ligne.moi_contrat_ob
                        contrat   += ligne.moi_contrat
                        client_obj    += ligne.moi_client_ob
                        client    += ligne.moi_client
                        reel_obj      += ligne.moi_reel_ob 
                        reel      += ligne.moi_reel
                        livraison_obj += ligne.moi_livraison_ob
                        livraison += ligne.moi_livraison
                        mat_obj +=ligne.moi_materiels_ob
                        mat += ligne.moi_materiels
                    rec.annee_chifre_ob = chiff_obj
                    rec.annee_chifre_aff = chiff
                    rec.annee_comer_ob = marge_obj
                    rec.annee_comer = marge
                    rec.annee_reel_ob = reel_obj
                    rec.annee_reel = reel
                    rec.annee_livraison_ob = livraison_obj
                    rec.annee_livraison = livraison
                    rec.anee_contrat_ob = contrat_obj
                    rec.anee_contrat = contrat
                    rec.annee_client_ob = client_obj
                    rec.annee_client = client
                    rec.annee_materiels_ob = mat_obj
                    rec.annee_materiels =  mat  

    def name_get(self):
        result = []
        for model in self:
            name = model.annee
            result.append((model.id, name))
        return result

    def refrech_po(self):
        for rec in self:
            #[('create_date', '&lt;',), ('create_date','&gt;=', date.time.strftime('rec.annee-01-01'))]
            date_debut = datetime(year=rec.annee, month=1, day=1)
            d1 = datetime.strftime(date_debut, "%Y-%m-%d %H:%M:%S")
            date_fin = datetime(year=rec.annee, month=12, day=31)
            d2 = datetime.strftime(date_fin, "%Y-%m-%d %H:%M:%S")
            #sale=self.env['sale.order'].search([('create_date', '&gt;=', date)])
            sale = self.env['sale.order'].sudo().search([('create_date', '>=', d1),('create_date', '<=', d2)])

            ########## par an
            somme_marge=0
            somme_chifre_aff =0
            somme_contrat = 0
            somme_client = 0
            somme_reel = 0
            somme_livraison = 0
            somme_materiel = 0
            ########## le moi janvier
            somme_janvier_marge = 0
            somme_janvier_chifre_aff = 0
            somme_janvier_contrat = 0
            somme_janvier_client = 0
            somme_janvier_reel = 0
            somme_janvier_livraison = 0
            somme_janvier_materiel = 0
            janvier_ok = False
            ########## le moi Février
            somme_fevrier_marge = 0
            somme_fevrier_chifre_aff = 0
            somme_fevrier_contrat = 0
            somme_fevrier_client = 0
            somme_fevrier_reel = 0
            somme_fevrier_livraison = 0
            somme_fevrier_materiel = 0
            fevrier_ok = False
            ########## le moi mars
            somme_mars_marge = 0
            somme_mars_chifre_aff = 0
            somme_mars_contrat = 0
            somme_mars_client = 0
            somme_mars_reel = 0
            somme_mars_livraison = 0
            somme_mars_materiel = 0
            mars_ok = False
            ########## le moi avril
            somme_avril_marge = 0
            somme_avril_chifre_aff = 0
            somme_avril_contrat = 0
            somme_avril_client = 0
            somme_avril_reel = 0
            somme_avril_livraison = 0
            somme_avril_materiel = 0
            avril_ok = False
            ########## le moi mai
            somme_mai_marge = 0
            somme_mai_chifre_aff = 0
            somme_mai_contrat = 0
            somme_mai_client = 0
            somme_mai_reel = 0
            somme_mai_livraison = 0
            somme_mai_materiel = 0
            mai_ok = False
            ########## le moi juin
            somme_juin_marge = 0
            somme_juin_chifre_aff = 0
            somme_juin_contrat = 0
            somme_juin_client = 0
            somme_juin_reel = 0
            somme_juin_livraison = 0
            somme_juin_materiel = 0
            juin_ok = False
            ########## le moi juillet
            somme_juillet_marge = 0
            somme_juillet_chifre_aff = 0
            somme_juillet_contrat = 0
            somme_juillet_client = 0
            somme_juillet_reel = 0
            somme_juillet_livraison = 0
            somme_juillet_materiel = 0
            juillet_ok = False
            ########## le moi Août
            somme_aout_marge = 0
            somme_aout_chifre_aff = 0
            somme_aout_contrat = 0
            somme_aout_client = 0
            somme_aout_reel = 0
            somme_aout_livraison = 0
            somme_aout_materiel = 0
            aout_ok = False
            ########## le moi septembre
            somme_septembre_marge = 0
            somme_septembre_chifre_aff = 0
            somme_septembre_contrat = 0
            somme_septembre_client = 0
            somme_septembre_reel = 0
            somme_septembre_livraison = 0
            somme_septembre_materiel = 0
            septembre_ok = False
            ########## le moi octobre
            somme_octobre_marge = 0
            somme_octobre_chifre_aff = 0
            somme_octobre_contrat = 0
            somme_octobre_client = 0
            somme_octobre_reel = 0
            somme_octobre_livraison = 0
            somme_octobre_materiel = 0
            octobre_ok = False
            ########## le moi novembre
            somme_novembre_marge =0
            somme_novembre_chifre_aff = 0
            somme_novembre_contrat = 0
            somme_novembre_client = 0
            somme_novembre_reel = 0
            somme_novembre_livraison = 0
            somme_novembre_materiel = 0
            novembre_ok    =False
            ########## le moi Décembre  decembre
            somme_decembre_marge = 0
            somme_decembre_chifre_aff = 0
            somme_decembre_contrat = 0
            somme_decembre_client = 0
            somme_decembre_reel = 0
            somme_decembre_livraison = 0
            somme_decembre_materiel = 0
            decembre_ok = False

            for sal in sale:
                print("create_date", sal.create_date.month)
                team_vente = False
                for record in sal.user_id.crm_team_ids:
                    if record.id == rec.annee_team.id:
                        team_vente = record
                if team_vente:
                    somme_marge += sal.x_studio_marge_commerciale
                    somme_chifre_aff += sal.sale_finance
                    somme_contrat += sal.sale_new_contrat
                    somme_client += sal.sale_new_contact
                    somme_reel += sal.x_studio_marge_relle
                    somme_livraison += sal.sale_frais
                    somme_materiel += sal.sale_materiels_vendu
                    if sal.create_date.month == 1:
                        ########## le moi janvier
                        somme_janvier_marge += sal.x_studio_marge_commerciale
                        somme_janvier_chifre_aff += sal.sale_finance
                        somme_janvier_contrat += sal.sale_new_contrat
                        somme_janvier_client += sal.sale_new_contact
                        somme_janvier_reel += sal.x_studio_marge_relle
                        somme_janvier_livraison += sal.sale_frais
                        somme_janvier_materiel += sal.sale_materiels_vendu                        
                        janvier_ok = True
                    if sal.create_date.month == 2:
                        ########## le moi Février
                        somme_fevrier_marge += sal.x_studio_marge_commerciale
                        somme_fevrier_chifre_aff += sal.sale_finance
                        somme_fevrier_contrat += sal.sale_new_contrat
                        somme_fevrier_client += sal.sale_new_contact
                        somme_fevrier_reel += sal.x_studio_marge_relle
                        somme_fevrier_livraison += sal.sale_frais
                        somme_fevrier_materiel += sal.sale_materiels_vendu  
                       
                        fevrier_ok = True
                    if sal.create_date.month == 3:
                        ########## le moi mars
                        somme_mars_marge += sal.x_studio_marge_commerciale
                        somme_mars_chifre_aff += sal.sale_finance
                        somme_mars_contrat += sal.sale_new_contrat
                        somme_mars_client += sal.sale_new_contact
                        
                        somme_mars_reel += sal.x_studio_marge_relle
                        somme_mars_livraison += sal.sale_frais
                        somme_mars_materiel += sal.sale_materiels_vendu
                        
                        mars_ok = True
                    if sal.create_date.month == 4:
                        ########## le moi avril
                        somme_avril_marge += sal.x_studio_marge_commerciale
                        somme_avril_chifre_aff += sal.sale_finance
                        somme_avril_contrat += sal.sale_new_contrat
                        somme_avril_client += sal.sale_new_contact
                        
                        somme_avril_reel += sal.x_studio_marge_relle
                        somme_avril_livraison += sal.sale_frais
                        somme_avril_materiel += sal.sale_materiels_vendu
                        
                        
                        avril_ok = True
                    if sal.create_date.month == 5:
                        ########## le moi mai
                        somme_mai_marge += sal.x_studio_marge_commerciale
                        somme_mai_chifre_aff += sal.sale_finance
                        somme_mai_contrat += sal.sale_new_contrat
                        somme_mai_client += sal.sale_new_contact
                        
                        somme_mai_reel += sal.x_studio_marge_relle
                        somme_mai_livraison += sal.sale_frais
                        somme_mai_materiel += sal.sale_materiels_vendu
                         
                        mai_ok = True
                    if sal.create_date.month == 6:
                        ########## le moi juin
                        somme_juin_marge += sal.x_studio_marge_commerciale
                        somme_juin_chifre_aff += sal.sale_finance
                        somme_juin_contrat += sal.sale_new_contrat
                        somme_juin_client += sal.sale_new_contact
                        
                        somme_juin_reel += sal.x_studio_marge_relle
                        somme_juin_livraison += sal.sale_frais
                        somme_juin_materiel += sal.sale_materiels_vendu
                        
                        
                        juin_ok = True
                    if sal.create_date.month == 7:
                        ########## le moi juillet
                        somme_juillet_marge += sal.x_studio_marge_commerciale
                        somme_juillet_chifre_aff += sal.sale_finance
                        somme_juillet_contrat += sal.sale_new_contrat
                        somme_juillet_client += sal.sale_new_contact
                        
                        somme_juillet_reel += sal.x_studio_marge_relle
                        somme_juillet_livraison += sal.sale_frais
                        somme_juillet_materiel += sal.sale_materiels_vendu
                        
                        juillet_ok = True
                    if sal.create_date.month == 8:
                        ########## le moi Août
                        somme_aout_marge += sal.x_studio_marge_commerciale
                        somme_aout_chifre_aff += sal.sale_finance
                        somme_aout_contrat += sal.sale_new_contrat
                        somme_aout_client += sal.sale_new_contact
                        
                        somme_aout_reel += sal.x_studio_marge_relle
                        somme_aout_livraison += sal.sale_frais
                        somme_aout_materiel += sal.sale_materiels_vendu                        
                      
                        aout_ok = True
                    if sal.create_date.month == 9:
                        ########## le moi septembre
                        somme_septembre_marge += sal.x_studio_marge_commerciale
                        somme_septembre_chifre_aff += sal.sale_finance
                        somme_septembre_contrat += sal.sale_new_contrat
                        somme_septembre_client += sal.sale_new_contact
                        
                        somme_septembre_reel += sal.x_studio_marge_relle
                        somme_septembre_livraison += sal.sale_frais
                        somme_septembre_materiel += sal.sale_materiels_vendu                          
                        
                        septembre_ok = True
                    if sal.create_date.month == 10:
                        ########## le moi octobre
                        somme_octobre_marge += sal.x_studio_marge_commerciale
                        somme_octobre_chifre_aff += sal.sale_finance
                        somme_octobre_contrat += sal.sale_new_contrat
                        somme_octobre_client += sal.sale_new_contact
                        
                        somme_octobre_reel += sal.x_studio_marge_relle
                        somme_octobre_livraison += sal.sale_frais
                        somme_octobre_materiel += sal.sale_materiels_vendu    
                        
                        octobre_ok = True
                    if sal.create_date.month == 11:
                        ########## le moi novembre
                        somme_novembre_marge+=sal.x_studio_marge_commerciale
                        somme_novembre_chifre_aff+=sal.sale_finance
                        somme_novembre_contrat+=sal.sale_new_contrat
                        somme_novembre_client+=sal.sale_new_contact
                        
                        somme_novembre_reel += sal.x_studio_marge_relle
                        somme_novembre_livraison += sal.sale_frais
                        somme_novembre_materiel += sal.sale_materiels_vendu  
                       
                        novembre_ok = True
                    if sal.create_date.month == 12:
                        ########## le moi Décembre  decembre
                        somme_decembre_marge += sal.x_studio_marge_commerciale
                        somme_decembre_chifre_aff += sal.sale_finance
                        somme_decembre_contrat += sal.sale_new_contrat
                        somme_decembre_client += sal.sale_new_contact
                        
                        somme_decembre_reel += sal.x_studio_marge_relle
                        somme_decembre_livraison += sal.sale_frais
                        somme_decembre_materiel += sal.sale_materiels_vendu  
                        
                        decembre_ok = True        
            
            ## le moi janvier         
            
            if janvier_ok:
                janvier_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 1:
                        janvier_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_janvier_chifre_aff=somme_janvier_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_janvier_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_janvier_marge=somme_janvier_marge/mois.moi_comer_ob
                        else:
                            somme_janvier_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_janvier_contrat=somme_janvier_contrat/mois.moi_contrat_ob
                        else:
                            somme_janvier_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_janvier_client=somme_janvier_client/mois.moi_client_ob
                        else:
                            somme_janvier_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_janvier_reel=somme_janvier_reel/mois.moi_reel_ob
                        else:
                            somme_janvier_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_janvier_livraison=somme_janvier_livraison/mois.moi_livraison_ob
                        else:
                            somme_janvier_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_janvier_materiel=somme_janvier_materiel/mois.moi_materiels_ob
                        else:
                            somme_janvier_materiel = 0
                        
                if janvier_list:
                    janvier_list[0].moi_comer =somme_janvier_marge
                    janvier_list[0].moi_chifre_aff = somme_janvier_chifre_aff
                    janvier_list[0].moi_contrat = somme_janvier_contrat
                    janvier_list[0].moi_client = somme_janvier_client
                    janvier_list[0].moi_reel = somme_janvier_reel
                    janvier_list[0].moi_livraison = somme_janvier_livraison
                    janvier_list[0].moi_materiels = somme_janvier_materiel
                    print("janvier_list[0]",janvier_list[0])
                else:
                    new_janvier = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': 0,
                        #'moi_chifre_aff': somme_janvier_chifre_aff,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 1,
                    })
                    print("new_janvier", new_janvier)
            ## le moi fevrier
            if fevrier_ok:
                fevrier_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 2:
                        fevrier_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_fevrier_chifre_aff=somme_fevrier_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_fevrier_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_fevrier_marge=somme_fevrier_marge/mois.moi_comer_ob
                        else:
                            somme_fevrier_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_fevrier_contrat=somme_fevrier_contrat/mois.moi_contrat_ob
                        else:
                            somme_fevrier_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_fevrier_client=somme_fevrier_client/mois.moi_client_ob
                        else:
                            somme_fevrier_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_fevrier_reel=somme_fevrier_reel/mois.moi_reel_ob
                        else:
                            somme_fevrier_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_fevrier_livraison=somme_fevrier_livraison/mois.moi_livraison_ob
                        else:
                            somme_janvier_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_fevrier_materiel=somme_fevrier_materiel/mois.moi_materiels_ob
                        else:
                            somme_fevrier_materiel = 0
                         
                if fevrier_list:
                    fevrier_list[0].moi_comer =somme_fevrier_marge
                    fevrier_list[0].moi_chifre_aff = somme_fevrier_chifre_aff
                    fevrier_list[0].moi_contrat = somme_fevrier_contrat
                    fevrier_list[0].moi_client = somme_fevrier_client
                    fevrier_list[0].moi_reel = somme_fevrier_reel
                    fevrier_list[0].moi_livraison = somme_fevrier_livraison
                    fevrier_list[0].moi_materiels = somme_fevrier_materiel
                    print("fevrier_list[0]",fevrier_list[0])
                else:
                    new_fevrier = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        #'moi_comer': somme_fevrier_marge,
                        'moi_comer': 0,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 2,
                    })
                    print("new_fevrier", new_fevrier)
            #### le moi  mars
            if mars_ok:
                mars_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 3:
                        mars_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_mars_chifre_aff=somme_mars_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_mars_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_mars_marge=somme_mars_marge/mois.moi_comer_ob
                        else:
                            somme_mars_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_mars_contrat=somme_mars_contrat/mois.moi_contrat_ob
                        else:
                            somme_mars_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_mars_client=somme_mars_client/mois.moi_client_ob
                        else:
                            somme_mars_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_mars_reel=somme_mars_reel/mois.moi_reel_ob
                        else:
                            somme_mars_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_mars_livraison=somme_mars_livraison/mois.moi_livraison_ob
                        else:
                            somme_mars_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_mars_materiel=somme_mars_materiel/mois.moi_materiels_ob
                        else:
                            somme_mars_materiel = 0
                        
                        
                if mars_list:
                    mars_list[0].moi_comer =somme_mars_marge
                    mars_list[0].moi_chifre_aff = somme_mars_chifre_aff
                    mars_list[0].moi_contrat = somme_mars_contrat
                    mars_list[0].moi_client = somme_mars_client
                    mars_list[0].moi_reel = somme_mars_reel
                    mars_list[0].moi_livraison = somme_mars_livraison
                    mars_list[0].moi_materiels = somme_mars_materiel
                    print("mars_list[0]",mars_list[0])
                else:
                    new_mars = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': 0,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 3,
                    })
                    print("new_mars", new_mars)
            #### le moi  avril
            if avril_ok:
                avril_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 4:
                        avril_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_avril_chifre_aff=somme_avril_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_avril_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_avril_marge=somme_avril_marge/mois.moi_comer_ob
                        else:
                            somme_avril_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_avril_contrat=somme_avril_contrat/mois.moi_contrat_ob
                        else:
                            somme_avril_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_avril_client=somme_avril_client/mois.moi_client_ob
                        else:
                            somme_avril_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_avril_reel=somme_avril_reel/mois.moi_reel_ob
                        else:
                            somme_avril_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_avril_livraison=somme_avril_livraison/mois.moi_livraison_ob
                        else:
                            somme_avril_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_avril_materiel=somme_avril_materiel/mois.moi_materiels_ob
                        else:
                            somme_avril_materiel = 0
                      
                if avril_list:
                    avril_list[0].moi_comer =somme_avril_marge
                    avril_list[0].moi_chifre_aff = somme_avril_chifre_aff
                    avril_list[0].moi_contrat = somme_avril_contrat
                    avril_list[0].moi_client = somme_avril_client
                    avril_list[0].moi_reel = somme_avril_reel
                    avril_list[0].moi_livraison = somme_avril_livraison
                    avril_list[0].moi_materiels = somme_avril_materiel
                    print("avril_list[0]",avril_list[0])
                else:
                    new_avril = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': 0,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 4,
                    })
                    print("new_avril", new_avril)
            #### le moi  mai
            if mai_ok:
                mai_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 5:
                        mai_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_mai_chifre_aff=somme_mai_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_mai_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_mai_marge=somme_mai_marge/mois.moi_comer_ob
                        else:
                            somme_mai_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_mai_contrat=somme_mai_contrat/mois.moi_contrat_ob
                        else:
                            somme_mai_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_mai_client=somme_mai_client/mois.moi_client_ob
                        else:
                            somme_mai_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_mai_reel=somme_mai_reel/mois.moi_reel_ob
                        else:
                            somme_mai_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_mai_livraison=somme_mai_livraison/mois.moi_livraison_ob
                        else:
                            somme_mai_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_mai_materiel=somme_mai_materiel/mois.moi_materiels_ob
                        else:
                            somme_mai_materiel = 0
                        
                if mai_list:
                    mai_list[0].moi_comer =somme_mai_marge
                    mai_list[0].moi_chifre_aff = somme_mai_chifre_aff
                    mai_list[0].moi_contrat = somme_mai_contrat
                    mai_list[0].moi_client = somme_mai_client
                    mai_list[0].moi_reel = somme_mai_reel
                    mai_list[0].moi_livraison = somme_mai_livraison
                    mai_list[0].moi_materiels = somme_mai_materiel
                    print("mai_list[0]",mai_list[0])
                else:
                    new_mai = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': 0,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 5,
                    })
                    print("new_mai", new_mai)
            ## le moi  juin
            if juin_ok:
                juin_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 6:
                        juin_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_juin_chifre_aff=somme_juin_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_juin_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_juin_marge=somme_juin_marge/mois.moi_comer_ob
                        else:
                            somme_juin_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_juin_contrat=somme_juin_contrat/mois.moi_contrat_ob
                        else:
                            somme_juin_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_juin_client=somme_juin_client/mois.moi_client_ob
                        else:
                            somme_juin_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_juin_reel=somme_juin_reel/mois.moi_reel_ob
                        else:
                            somme_juin_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_juin_livraison=somme_juin_livraison/mois.moi_livraison_ob
                        else:
                            somme_juin_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_juin_materiel=somme_juin_materiel/mois.moi_materiels_ob
                        else:
                            somme_juin_materiel = 0
            
                if juin_list:
                    juin_list[0].moi_comer =somme_juin_marge
                    juin_list[0].moi_chifre_aff = somme_juin_chifre_aff
                    juin_list[0].moi_contrat = somme_juin_contrat
                    juin_list[0].moi_client = somme_juin_client
                    juin_list[0].moi_reel = somme_juin_reel
                    juin_list[0].moi_livraison = somme_juin_livraison
                    juin_list[0].moi_materiels = somme_juin_materiel
                    print("juin_list[0]",juin_list[0])
                else:
                    new_juin = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': 0,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 6,
                    })
                    print("new_juin", new_juin)
            ###########
            ## le moi  juillet
            if juillet_ok:
                juillet_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 7:
                        juillet_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_juillet_chifre_aff=somme_juillet_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_juillet_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_juillet_marge=somme_juillet_marge/mois.moi_comer_ob
                        else:
                            somme_juillet_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_juin_contrat=somme_juin_contrat/mois.moi_contrat_ob
                        else:
                            somme_juillet_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_juillet_client=somme_juillet_client/mois.moi_client_ob
                        else:
                            somme_juillet_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_juillet_reel=somme_juillet_reel/mois.moi_reel_ob
                        else:
                            somme_juillet_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_juillet_livraison=somme_juillet_livraison/mois.moi_livraison_ob
                        else:
                            somme_juillet_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_juillet_materiel=somme_juillet_materiel/mois.moi_materiels_ob
                        else:
                            somme_juillet_materiel = 0
                        
                        
                        
                if juillet_list:
                    juillet_list[0].moi_comer =somme_juillet_marge
                    juillet_list[0].moi_chifre_aff = somme_juillet_chifre_aff
                    juillet_list[0].moi_contrat = somme_juillet_contrat
                    juillet_list[0].moi_client = somme_juillet_client
                    juillet_list[0].moi_reel = somme_juillet_reel
                    juillet_list[0].moi_livraison = somme_juillet_livraison
                    juillet_list[0].moi_materiels = somme_juillet_materiel
                    print("juillet_list[0]",juillet_list[0])
                else:
                    new_juillet = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': 0,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 7,
                    })
                    print("new_juillet", new_juillet)
            ###########


            ## le moi  aout
            if aout_ok:
                aout_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 8:
                        aout_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_aout_chifre_aff=somme_aout_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_aout_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_aout_marge=somme_aout_marge/mois.moi_comer_ob
                        else:
                            somme_aout_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_aout_contrat=somme_aout_contrat/mois.moi_contrat_ob
                        else:
                            somme_aout_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_aout_client=somme_aout_client/mois.moi_client_ob
                        else:
                            somme_aout_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_aout_reel=somme_aout_reel/mois.moi_reel_ob
                        else:
                            somme_aout_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_aout_livraison=somme_aout_livraison/mois.moi_livraison_ob
                        else:
                            somme_aout_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_aout_materiel=somme_aout_materiel/mois.moi_materiels_ob
                        else:
                            somme_aout_materiel = 0
                       
                if aout_list:
                    aout_list[0].moi_comer =somme_aout_marge
                    aout_list[0].moi_chifre_aff = somme_aout_chifre_aff
                    aout_list[0].moi_contrat = somme_aout_contrat
                    aout_list[0].moi_client = somme_aout_client
                    aout_list[0].moi_reel = somme_aout_reel
                    aout_list[0].moi_livraison = somme_aout_livraison
                    aout_list[0].moi_materiels = somme_aout_materiel
                    print("aout_list[0]",aout_list[0])
                else:
                    new_aout = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': 0,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 8,
                    })
                    print("new_aout", new_aout)
            ###########
            ## le moi  septembre
            if septembre_ok:
                septembre_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 9:
                        septembre_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_septembre_chifre_aff=somme_septembre_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_septembre_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_septembre_marge=somme_septembre_marge/mois.moi_comer_ob
                        else:
                            somme_septembre_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_septembre_contrat=somme_septembre_contrat/mois.moi_contrat_ob
                        else:
                            somme_septembre_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_septembre_client=somme_septembre_client/mois.moi_client_ob
                        else:
                            somme_septembre_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_septembre_reel=somme_septembre_reel/mois.moi_reel_ob
                        else:
                            somme_septembre_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_septembre_livraison=somme_septembre_livraison/mois.moi_livraison_ob
                        else:
                            somme_septembre_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_septembre_materiel=somme_septembre_materiel/mois.moi_materiels_ob
                        else:
                            somme_septembre_materiel = 0
                        
                        
                if septembre_list:
                    septembre_list[0].moi_comer =somme_septembre_marge
                    septembre_list[0].moi_chifre_aff = somme_septembre_chifre_aff
                    septembre_list[0].moi_contrat = somme_septembre_contrat
                    septembre_list[0].moi_client = somme_septembre_client
                    septembre_list[0].moi_reel = somme_septembre_reel
                    septembre_list[0].moi_livraison = somme_septembre_livraison
                    septembre_list[0].moi_materiels = somme_septembre_materiel
                    print("septembre_list[0]",septembre_list[0])
                else:
                    new_septembre = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': 0,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 9,
                    })
                    print("new_septembre", new_septembre)
            ###########

            ## le moi  octobre
            if octobre_ok:
                octobre_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 10:
                        octobre_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_octobre_chifre_aff=somme_octobre_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_octobre_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_octobre_marge=somme_octobre_marge/mois.moi_comer_ob
                        else:
                            somme_octobre_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_octobre_contrat=somme_octobre_contrat/mois.moi_contrat_ob
                        else:
                            somme_octobre_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_octobre_client=somme_octobre_client/mois.moi_client_ob
                        else:
                            somme_octobre_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_octobre_reel=somme_octobre_reel/mois.moi_reel_ob
                        else:
                            somme_octobre_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_octobre_livraison=somme_octobre_livraison/mois.moi_livraison_ob
                        else:
                            somme_octobre_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_octobre_materiel=somme_octobre_materiel/mois.moi_materiels_ob
                        else:
                            somme_octobre_materiel = 0
                            
                      
                if octobre_list:
                    octobre_list[0].moi_comer =somme_octobre_marge
                    octobre_list[0].moi_chifre_aff = somme_octobre_chifre_aff
                    octobre_list[0].moi_contrat = somme_octobre_contrat
                    octobre_list[0].moi_client = somme_octobre_client
                    octobre_list[0].moi_reel = somme_octobre_reel
                    octobre_list[0].moi_livraison = somme_octobre_livraison
                    octobre_list[0].moi_materiels = somme_octobre_materiel
                    print("octobre_list[0]",octobre_list[0])
                else:
                    new_octobre = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': 0,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 10,
                    })
                    print("new_octobre", new_octobre)
            ###########

            ## le moi  novembre
            if novembre_ok:
                novembre_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 11:
                        novembre_list.append(mois)
                        ##par chifre_aff
                        if mois.moi_chifre_aff_ob>0:
                            somme_novembre_chifre_aff=somme_novembre_chifre_aff/mois.moi_chifre_aff_ob
                        else:
                            somme_novembre_chifre_aff = 0      
                        ##par marge com
                        if mois.moi_comer_ob>0:
                            somme_novembre_marge=somme_novembre_marge/mois.moi_comer_ob
                        else:
                            somme_novembre_marge = 0  
                        ##par contrat
                        if mois.moi_contrat_ob>0:
                            somme_novembre_contrat=somme_novembre_contrat/mois.moi_contrat_ob
                        else:
                            somme_novembre_contrat = 0                         
                         ##par client
                        if mois.moi_client_ob>0:
                            somme_novembre_client=somme_novembre_client/mois.moi_client_ob
                        else:
                            somme_novembre_client = 0
                        ##par reel
                        if mois.moi_reel_ob>0:
                            somme_novembre_reel=somme_novembre_reel/mois.moi_reel_ob
                        else:
                            somme_novembre_reel = 0
                        ##par livraison
                        if mois.moi_livraison_ob>0:
                            somme_novembre_livraison=somme_novembre_livraison/mois.moi_livraison_ob
                        else:
                            somme_novembre_livraison = 0
                        ##par materiels
                        if mois.moi_materiels_ob>0:
                            somme_novembre_materiel=somme_novembre_materiel/mois.moi_materiels_ob
                        else:
                            somme_novembre_materiel = 0
                       
                if novembre_list:
                    novembre_list[0].moi_comer =somme_novembre_marge
                    novembre_list[0].moi_chifre_aff = somme_novembre_chifre_aff
                    novembre_list[0].moi_contrat = somme_novembre_contrat
                    novembre_list[0].moi_client = somme_novembre_client
                    novembre_list[0].moi_reel = somme_novembre_reel
                    novembre_list[0].moi_livraison = somme_novembre_livraison
                    novembre_list[0].moi_materiels = somme_novembre_materiel
                    print("novembre_list[0]",novembre_list[0])
                else:
                    new_novembre = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': 0,
                        'moi_chifre_aff': 0,
                        'moi_contrat': 0,
                        'moi_client': 0,
                        'moi_reel': 0,
                        'moi_livraison': 0,
                        'moi_materiels': 0,
                        'mois_int': 11,
                    })
                    print("new_novembre", new_novembre)
            ###########
            ## le moi  decembre
            if decembre_ok:
                        decembre_list = []
                        for mois in rec.mois:
                            if mois.mois_int == 12:
                                decembre_list.append(mois)
                                ##par chifre_aff
                                if mois.moi_chifre_aff_ob>0:
                                    somme_decembre_chifre_aff=somme_decembre_chifre_aff/mois.moi_chifre_aff_ob
                                else:
                                    somme_decembre_chifre_aff = 0      
                                ##par marge com
                                if mois.moi_comer_ob>0:
                                    somme_decembre_marge=somme_decembre_marge/mois.moi_comer_ob
                                else:
                                    somme_decembre_marge = 0  
                                ##par contrat
                                if mois.moi_contrat_ob>0:
                                    somme_decembre_contrat=somme_decembre_contrat/mois.moi_contrat_ob
                                else:
                                    somme_decembre_contrat = 0                         
                                 ##par client
                                if mois.moi_client_ob>0:
                                    somme_decembre_client=somme_decembre_client/mois.moi_client_ob
                                else:
                                    somme_decembre_client = 0
                                ##par reel
                                if mois.moi_reel_ob>0:
                                    somme_decembre_reel=somme_decembre_reel/mois.moi_reel_ob
                                else:
                                    somme_decembre_reel = 0
                                ##par livraison
                                if mois.moi_livraison_ob>0:
                                    somme_decembre_livraison=somme_decembre_livraison/mois.moi_livraison_ob
                                else:
                                    somme_decembre_livraison = 0
                                ##par materiels
                                if mois.moi_materiels_ob>0:
                                    somme_decembre_materiel=somme_decembre_materiel/mois.moi_materiels_ob
                                else:
                                    somme_decembre_materiel = 0                               
                                
                                
                        if decembre_list:
                            decembre_list[0].moi_comer = somme_decembre_marge
                            decembre_list[0].moi_chifre_aff = somme_decembre_chifre_aff
                            decembre_list[0].moi_contrat = somme_decembre_contrat
                            decembre_list[0].moi_client = somme_decembre_client
                            decembre_list[0].moi_reel = somme_decembre_reel
                            decembre_list[0].moi_livraison = somme_decembre_livraison
                            decembre_list[0].moi_materiels = somme_decembre_materiel
                            print("decembre_list[0]", decembre_list[0])
                        else:
                            new_decembre = self.env['moisvente'].sudo().create({
                                'annee': rec.id,
                                'moi_comer': 0,
                                'moi_chifre_aff': 0,
                                'moi_contrat': 0,
                                'moi_client': 0,
                                'moi_reel': 0,
                                'moi_livraison': 0,
                                'moi_materiels': 0,
                                'mois_int': 12,
                            })
                            print("new_decembre", new_decembre)            
            
            
            #rec.annee_chifre_aff = somme_chifre_aff
            #rec.annee_comer = somme_marge
            #rec.anee_contrat = somme_contrat
            #rec.annee_client = somme_client
            #rec.annee_reel = somme_reel   
            #rec.annee_livraison = somme_livraison
            #rec.annee_materiels = somme_materiel
            
                    
            
 

class Moismodel(models.Model):
    _name        = 'moisvente'
    _description = 'stat par mois'
    mois         = fields.Char('Mois', default='Janvier', compute="convert_mois")
    mois_int     = fields.Integer("Numéro", default=1)
    annee        = fields.Many2one( "anneevente",string='Année')
    moi_chifre_aff_ob = fields.Float(string="Obj CA")
    moi_chifre_aff = fields.Float(string="%", readonly=True)
    moi_comer_ob = fields.Float(string="Obj MC") 
    moi_comer = fields.Float(string="%", readonly=True) 
    moi_reel_ob = fields.Float(string="Obj MR") 
    moi_reel = fields.Float(string="%", readonly=True) 
    moi_livraison_ob = fields.Float(string="Obj FL") 
    moi_livraison = fields.Float(string="%", readonly=True) 
    moi_contrat_ob = fields.Float(string="Obj NB CONTRAT")
    moi_contrat = fields.Float(string="%", readonly=True)
    moi_client_ob = fields.Float(string="Obj NB NEW")
    moi_client = fields.Float(string="%", readonly=True)
    moi_materiels_ob = fields.Float(string="Obj NB MATERIELS")
    moi_materiels = fields.Float(string="%", readonly=True)

    @api.depends('mois_int')
    def convert_mois(self):
        for rec in self:
            if rec.mois_int ==1:
                rec.mois = "Janvier"
            if rec.mois_int ==2:
                rec.mois = "Février"
            if rec.mois_int ==3:
                rec.mois = "Mars"
            if rec.mois_int ==4:
                rec.mois = "Avril"
            if rec.mois_int == 5:
                rec.mois = "Mai"
            if rec.mois_int ==6:
                rec.mois = "Juin"
            if rec.mois_int ==7:
                rec.mois = "Juillet"
            if rec.mois_int ==8:
                rec.mois = "Août"
            if rec.mois_int ==9:
                rec.mois = "Septembre"
            if rec.mois_int ==10:
                rec.mois = "Octobre"
            if rec.mois_int ==11:
                rec.mois = "Novembre"
            if rec.mois_int ==12:
                rec.mois = "Décembre"


