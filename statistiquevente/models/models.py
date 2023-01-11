from odoo import _, api, fields, models
from datetime import date,datetime

from dateutil.relativedelta import relativedelta

class   Anneemodel(models.Model):
    _name = "anneevente"
    _description = 'stat par an'
    annee = fields.Integer("Année",default=2023)
    mois = fields.One2many('moisvente', inverse_name='annee',string="Mois", readonly=True)
    annee_comer = fields.Float(string="%Marge comercial total")
    annee_chifre_aff = fields.Float(string="%Chiffre d'affaire total")
    anee_contrat = fields.Float(string="%Nombre de contrats total")
    annee_client = fields.Float(string="%Nombre de clients total")

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
            ########## le moi janvier
            somme_janvier_marge = 0
            somme_janvier_chifre_aff = 0
            somme_janvier_contrat = 0
            somme_janvier_client = 0
            janvier_ok = False
            ########## le moi Février
            somme_fevrier_marge = 0
            somme_fevrier_chifre_aff = 0
            somme_fevrier_contrat = 0
            somme_fevrier_client = 0
            fevrier_ok = False
            ########## le moi mars
            somme_mars_marge = 0
            somme_mars_chifre_aff = 0
            somme_mars_contrat = 0
            somme_mars_client = 0
            mars_ok = False
            ########## le moi avril
            somme_avril_marge = 0
            somme_avril_chifre_aff = 0
            somme_avril_contrat = 0
            somme_avril_client = 0
            avril_ok = False
            ########## le moi mai
            somme_mai_marge = 0
            somme_mai_chifre_aff = 0
            somme_mai_contrat = 0
            somme_mai_client = 0
            mai_ok = False
            ########## le moi juin
            somme_juin_marge = 0
            somme_juin_chifre_aff = 0
            somme_juin_contrat = 0
            somme_juin_client = 0
            juin_ok = False
            ########## le moi juillet
            somme_juillet_marge = 0
            somme_juillet_chifre_aff = 0
            somme_juillet_contrat = 0
            somme_juillet_client = 0
            juillet_ok = False
            ########## le moi Août
            somme_aout_marge = 0
            somme_aout_chifre_aff = 0
            somme_aout_contrat = 0
            somme_aout_client = 0
            aout_ok = False
            ########## le moi septembre
            somme_septembre_marge = 0
            somme_septembre_chifre_aff = 0
            somme_septembre_contrat = 0
            somme_septembre_client = 0
            septembre_ok = False
            ########## le moi octobre
            somme_octobre_marge = 0
            somme_octobre_chifre_aff = 0
            somme_octobre_contrat = 0
            somme_octobre_client = 0
            octobre_ok = False
            ########## le moi novembre
            somme_novembre_marge =0
            somme_novembre_chifre_aff = 0
            somme_novembre_contrat = 0
            somme_novembre_client = 0
            novembre_ok    =False
            ########## le moi Décembre  decembre
            somme_decembre_marge = 0
            somme_decembre_chifre_aff = 0
            somme_decembre_contrat = 0
            somme_decembre_client = 0
            decembre_ok = False

            for sal in sale:
                print("create_date", sal.create_date.month)
                team_vente = False
                for record in sal.user_id.crm_team_ids:
                    if record.id == 1:
                        team_vente = record
                if team_vente:
                    somme_marge += sal.x_studio_marge_comer_tot_fin
                    somme_chifre_aff += sal.x_studio_chifre_affaire_total
                    somme_contrat += sal.x_studio_nombre_contrat_tot
                    somme_client += sal.x_studio_nombre_tot_client_stat
                    if sal.create_date.month == 1:
                        ########## le moi janvier
                        somme_janvier_marge += sal.x_studio_marge_comer_tot_fin
                        somme_janvier_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_janvier_contrat += sal.x_studio_nombre_contrat_tot
                        somme_janvier_client += sal.x_studio_nombre_tot_client_stat
                        janvier_ok = True
                    if sal.create_date.month == 2:
                        ########## le moi Février
                        somme_fevrier_marge += sal.x_studio_marge_comer_tot_fin
                        somme_fevrier_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_fevrier_contrat += sal.x_studio_nombre_contrat_tot
                        somme_fevrier_client += sal.x_studio_nombre_tot_client_stat
                        fevrier_ok = True
                    if sal.create_date.month == 3:
                        ########## le moi mars
                        somme_mars_marge += sal.x_studio_marge_comer_tot_fin
                        somme_mars_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_mars_contrat += sal.x_studio_nombre_contrat_tot
                        somme_mars_client += sal.x_studio_nombre_tot_client_stat
                        mars_ok = True
                    if sal.create_date.month == 4:
                        ########## le moi avril
                        somme_avril_marge += sal.x_studio_marge_comer_tot_fin
                        somme_avril_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_avril_contrat += sal.x_studio_nombre_contrat_tot
                        somme_avril_client += sal.x_studio_nombre_tot_client_stat
                        avril_ok = True
                    if sal.create_date.month == 5:
                        ########## le moi mai
                        somme_mai_marge += sal.x_studio_marge_comer_tot_fin
                        somme_mai_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_mai_contrat += sal.x_studio_nombre_contrat_tot
                        somme_mai_client += sal.x_studio_nombre_tot_client_stat
                        mai_ok = True
                    if sal.create_date.month == 6:
                        ########## le moi juin
                        somme_juin_marge += sal.x_studio_marge_comer_tot_fin
                        somme_juin_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_juin_contrat += sal.x_studio_nombre_contrat_tot
                        somme_juin_client += sal.x_studio_nombre_tot_client_stat
                        juin_ok = True
                    if sal.create_date.month == 7:
                        ########## le moi juillet
                        somme_juillet_marge += sal.x_studio_marge_comer_tot_fin
                        somme_juillet_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_juillet_contrat += sal.x_studio_nombre_contrat_tot
                        somme_juillet_client += sal.x_studio_nombre_tot_client_stat
                        juillet_ok = True
                    if sal.create_date.month == 8:
                        ########## le moi Août
                        somme_aout_marge += sal.x_studio_marge_comer_tot_fin
                        somme_aout_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_aout_contrat += sal.x_studio_nombre_contrat_tot
                        somme_aout_client += sal.x_studio_nombre_tot_client_stat
                        aout_ok = True
                    if sal.create_date.month == 9:
                        ########## le moi septembre
                        somme_septembre_marge += sal.x_studio_marge_comer_tot_fin
                        somme_septembre_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_septembre_contrat += sal.x_studio_nombre_contrat_tot
                        somme_septembre_client += sal.x_studio_nombre_tot_client_stat
                        septembre_ok = True
                    if sal.create_date.month == 10:
                        ########## le moi octobre
                        somme_octobre_marge += sal.x_studio_marge_comer_tot_fin
                        somme_octobre_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_octobre_contrat += sal.x_studio_nombre_contrat_tot
                        somme_octobre_client += sal.x_studio_nombre_tot_client_stat
                        octobre_ok = True
                    if sal.create_date.month == 11:
                        ########## le moi novembre
                        somme_novembre_marge+=sal.x_studio_marge_comer_tot_fin
                        somme_novembre_chifre_aff+=sal.x_studio_chifre_affaire_total
                        somme_novembre_contrat+=sal.x_studio_nombre_contrat_tot
                        somme_novembre_client+=sal.x_studio_nombre_tot_client_stat
                        novembre_ok = True
                    if sal.create_date.month == 12:
                        ########## le moi Décembre  decembre
                        somme_decembre_marge += sal.x_studio_marge_comer_tot_fin
                        somme_decembre_chifre_aff += sal.x_studio_chifre_affaire_total
                        somme_decembre_contrat += sal.x_studio_nombre_contrat_tot
                        somme_decembre_client += sal.x_studio_nombre_tot_client_stat
                        decembre_ok = True
            ##
            ## le moi janvier
            if janvier_ok:
                janvier_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 1:
                        janvier_list.append(mois)
                if janvier_list:
                    janvier_list[0].moi_comer =somme_janvier_marge
                    janvier_list[0].moi_chifre_aff = somme_janvier_chifre_aff
                    janvier_list[0].moi_contrat = somme_janvier_contrat
                    janvier_list[0].moi_client = somme_janvier_client
                    print("janvier_list[0]",janvier_list[0])
                else:
                    new_janvier = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_janvier_marge,
                        'moi_chifre_aff': somme_janvier_chifre_aff,
                        'moi_contrat': somme_janvier_contrat,
                        'moi_client': somme_janvier_client,
                        'mois_int': 1,
                    })
                    print("new_janvier", new_janvier)
            ## le moi fevrier
            if fevrier_ok:
                fevrier_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 2:
                        fevrier_list.append(mois)
                if fevrier_list:
                    fevrier_list[0].moi_comer =somme_fevrier_marge
                    fevrier_list[0].moi_chifre_aff = somme_fevrier_chifre_aff
                    fevrier_list[0].moi_contrat = somme_fevrier_contrat
                    fevrier_list[0].moi_client = somme_fevrier_client
                    print("fevrier_list[0]",fevrier_list[0])
                else:
                    new_fevrier = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_fevrier_marge,
                        'moi_chifre_aff': somme_fevrier_chifre_aff,
                        'moi_contrat': somme_fevrier_contrat,
                        'moi_client': somme_fevrier_client,
                        'mois_int': 2,
                    })
                    print("new_fevrier", new_fevrier)
            #### le moi  mars
            if mars_ok:
                mars_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 3:
                        mars_list.append(mois)
                if mars_list:
                    mars_list[0].moi_comer =somme_mars_marge
                    mars_list[0].moi_chifre_aff = somme_mars_chifre_aff
                    mars_list[0].moi_contrat = somme_mars_contrat
                    mars_list[0].moi_client = somme_mars_client
                    print("mars_list[0]",mars_list[0])
                else:
                    new_mars = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_mars_marge,
                        'moi_chifre_aff': somme_mars_chifre_aff,
                        'moi_contrat': somme_mars_contrat,
                        'moi_client': somme_mars_client,
                        'mois_int': 3,
                    })
                    print("new_mars", new_mars)
            #### le moi  avril
            if avril_ok:
                avril_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 4:
                        avril_list.append(mois)
                if avril_list:
                    avril_list[0].moi_comer =somme_avril_marge
                    avril_list[0].moi_chifre_aff = somme_avril_chifre_aff
                    avril_list[0].moi_contrat = somme_avril_contrat
                    avril_list[0].moi_client = somme_avril_client
                    print("avril_list[0]",avril_list[0])
                else:
                    new_avril = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_avril_marge,
                        'moi_chifre_aff': somme_avril_chifre_aff,
                        'moi_contrat': somme_avril_contrat,
                        'moi_client': somme_avril_client,
                        'mois_int': 4,
                    })
                    print("new_avril", new_avril)
            #### le moi  mai
            if mai_ok:
                mai_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 5:
                        mai_list.append(mois)
                if mai_list:
                    mai_list[0].moi_comer =somme_mai_marge
                    mai_list[0].moi_chifre_aff = somme_mai_chifre_aff
                    mai_list[0].moi_contrat = somme_mai_contrat
                    mai_list[0].moi_client = somme_mai_client
                    print("mai_list[0]",mai_list[0])
                else:
                    new_mai = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_mai_marge,
                        'moi_chifre_aff': somme_mai_chifre_aff,
                        'moi_contrat': somme_mai_contrat,
                        'moi_client': somme_mai_client,
                        'mois_int': 5,
                    })
                    print("new_mai", new_mai)
            ## le moi  juin
            if juin_ok:
                juin_list =[]
                for mois in rec.mois:
                    if mois.mois_int  == 6:
                        juin_list.append(mois)
                if juin_list:
                    juin_list[0].moi_comer =somme_juin_marge
                    juin_list[0].moi_chifre_aff = somme_juin_chifre_aff
                    juin_list[0].moi_contrat = somme_juin_contrat
                    juin_list[0].moi_client = somme_juin_client
                    print("juin_list[0]",juin_list[0])
                else:
                    new_juin = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_juin_marge,
                        'moi_chifre_aff': somme_juin_chifre_aff,
                        'moi_contrat': somme_juin_contrat,
                        'moi_client': somme_juin_client,
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
                if juillet_list:
                    juillet_list[0].moi_comer =somme_juillet_marge
                    juillet_list[0].moi_chifre_aff = somme_juillet_chifre_aff
                    juillet_list[0].moi_contrat = somme_juillet_contrat
                    juillet_list[0].moi_client = somme_juillet_client
                    print("juillet_list[0]",juillet_list[0])
                else:
                    new_juillet = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_juillet_marge,
                        'moi_chifre_aff': somme_juillet_chifre_aff,
                        'moi_contrat': somme_juillet_contrat,
                        'moi_client': somme_juillet_client,
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
                if aout_list:
                    aout_list[0].moi_comer =somme_aout_marge
                    aout_list[0].moi_chifre_aff = somme_aout_chifre_aff
                    aout_list[0].moi_contrat = somme_aout_contrat
                    aout_list[0].moi_client = somme_aout_client
                    print("aout_list[0]",aout_list[0])
                else:
                    new_aout = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_aout_marge,
                        'moi_chifre_aff': somme_aout_chifre_aff,
                        'moi_contrat': somme_aout_contrat,
                        'moi_client': somme_aout_client,
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
                if septembre_list:
                    septembre_list[0].moi_comer =somme_septembre_marge
                    septembre_list[0].moi_chifre_aff = somme_septembre_chifre_aff
                    septembre_list[0].moi_contrat = somme_septembre_contrat
                    septembre_list[0].moi_client = somme_septembre_client
                    print("septembre_list[0]",septembre_list[0])
                else:
                    new_septembre = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_septembre_marge,
                        'moi_chifre_aff': somme_septembre_chifre_aff,
                        'moi_contrat': somme_septembre_contrat,
                        'moi_client': somme_septembre_client,
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
                if octobre_list:
                    octobre_list[0].moi_comer =somme_octobre_marge
                    octobre_list[0].moi_chifre_aff = somme_octobre_chifre_aff
                    octobre_list[0].moi_contrat = somme_octobre_contrat
                    octobre_list[0].moi_client = somme_octobre_client
                    print("octobre_list[0]",octobre_list[0])
                else:
                    new_octobre = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_octobre_marge,
                        'moi_chifre_aff': somme_octobre_chifre_aff,
                        'moi_contrat': somme_octobre_contrat,
                        'moi_client': somme_octobre_client,
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
                if novembre_list:
                    novembre_list[0].moi_comer =somme_novembre_marge
                    novembre_list[0].moi_chifre_aff = somme_novembre_chifre_aff
                    novembre_list[0].moi_contrat = somme_novembre_contrat
                    novembre_list[0].moi_client = somme_novembre_client
                    print("novembre_list[0]",novembre_list[0])
                else:
                    new_novembre = self.env['moisvente'].sudo().create({
                        'annee': rec.id,
                        'moi_comer': somme_novembre_marge,
                        'moi_chifre_aff': somme_novembre_chifre_aff,
                        'moi_contrat': somme_novembre_contrat,
                        'moi_client': somme_novembre_client,
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
                        if decembre_list:
                            decembre_list[0].moi_comer = somme_decembre_marge
                            decembre_list[0].moi_chifre_aff = somme_decembre_chifre_aff
                            decembre_list[0].moi_contrat = somme_decembre_contrat
                            decembre_list[0].moi_client = somme_decembre_client
                            print("decembre_list[0]", decembre_list[0])
                        else:
                            new_decembre = self.env['moisvente'].sudo().create({
                                'annee': rec.id,
                                'moi_comer': somme_decembre_marge,
                                'moi_chifre_aff': somme_decembre_chifre_aff,
                                'moi_contrat': somme_decembre_contrat,
                                'moi_client': somme_decembre_client,
                                'mois_int': 12,
                            })
                            print("new_decembre", new_decembre)

            rec.annee_comer = somme_marge
            rec.annee_chifre_aff = somme_chifre_aff
            rec.anee_contrat = somme_contrat
            rec.annee_client = somme_client





class Moismodel(models.Model):
    _name        = 'moisvente'
    _description = 'stat par mois'
    mois         = fields.Char('Mois', default='Janvier', compute="convert_mois")
    mois_int     = fields.Integer("Numéro", default=1)
    annee        = fields.Many2one( "anneevente",string='Année')
    moi_comer = fields.Float(string="%Marge comercial total")
    moi_chifre_aff = fields.Float(string="%Chiffre d'affaire total")
    moi_contrat = fields.Float(string="%Nombre de contrats total")
    moi_client = fields.Float(string="%Nombre de clients total")

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


