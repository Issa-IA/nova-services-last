from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class factAuto(models.Model):
    _name = 'facturationauto'
    def create_facturation(self):
        list_client_par_dossier = {}
        list_client_tout_dossier = {}
        list_client_non_active_dossier = {}

        for rec in self.env['res.partner'].search([]):
            list_vente = {}
            list_vente_non_active = {}
            for vente in rec.sale_order_ids:
                list_fleet = []
                list_fleet_non_active = []
                for fleet in vente.sale_parc_ids:
                    id = self.env['fleet.vehicle.state'].search([('name', '=', "Inactif")])[0].id
                    if fleet.etat_serie == 'a_jour':
                        if fleet.state_id.id != id and fleet.fleet_date_inst <= date.today() <= fleet.fleet_expiration_date + relativedelta(days=1):
                            list_fleet.append(fleet)
                            fleet.etat_serie = 'n_ajour'
                    else:
                        if fleet.fleet_expiration_date:
                            print(id)
                            if fleet.state_id.id != id and fleet.fleet_date_inst <= date.today() <= fleet.fleet_expiration_date+ relativedelta(days=1) :
                                list_fleet_non_active.append(fleet)

                if list_fleet != []:
                    list_vente[vente] = list_fleet
                    vente.devis_a_cree_commande = False
                if list_fleet_non_active != []:
                    vente.devis_a_cree_commande = True
                    list_vente_non_active[vente] = list_fleet_non_active



            if list_vente != {}:

                print('type', rec.type_facture)
                if rec.type_facture == 'par_dossier':
                    list_client_par_dossier[rec] = list_vente
                if rec.type_facture == 'tout_dossiers':
                    list_client_tout_dossier[rec] = list_vente
            if list_vente_non_active != {}:
                list_client_non_active_dossier[rec]=list_vente_non_active


        print('par dossier',list_client_par_dossier)
        print('tout dossier', list_client_tout_dossier)
        print('list_client_non_active_dossier',list_client_non_active_dossier)



        #################### par dossier

        for i in list_client_par_dossier.items():
            purchase_id = False
            print(i[0].name)
            list_numero_dossier_par_dossier = []
            for j in i[1].items():
                if j[0].sale_dossier not in list_numero_dossier_par_dossier:
                    list_numero_dossier_par_dossier.append(j[0].sale_dossier)
                    sale_vals = {
                        'company_id': j[0].company_id.id,
                        'date_order': datetime.now(),
                        'partner_id': j[0].partner_id.id,
                        'partner_invoice_id': j[0].partner_invoice_id.id,
                        'partner_shipping_id': j[0].partner_shipping_id.id,
                        'picking_policy': j[0].picking_policy,
                        'pricelist_id': j[0].pricelist_id.id,
                        'warehouse_id': j[0].warehouse_id.id,
                        'state': 'sale',
                        'sale_maintnance':True,
                    }
                    purchase_id1 = self.env['sale.order'].sudo().create(sale_vals)
                    purchase_id = purchase_id1.id
                    print(purchase_id)
                    print(purchase_id1.sale_maintnance)
                    res = {
                        'order_id': purchase_id,
                        'display_type': 'line_section',
                        'name': "Dossier N°"+str(j[0].sale_dossier),
                    }
                    self.env['sale.order.line'].sudo().create(res)

                qte_by_dossier_forfait_coleur = 0
                qte_by_dossier_forfait_noir = 0
                qte_by_dossier_sup_coleur = 0
                qte_by_dossier_sup_noir = 0
                qte_by_dossier_abonnement_service = 0
                qte_by_dossier_autre = 0


                for k in j[1]:
                    ######### create devis fleet liste
                    res = {
                        'fleet_id': k.id,
                        'devis_id': purchase_id,
                        'comp_couleur_diff':k.comp_couleur_diff,
                        'comp_noir_diff': k.comp_noir_diff,
                    }
                    self.env['listboncommandefleet'].sudo().create(res)
                    ################### fin


                    qte_by_dossier_forfait_coleur +=  k.fleet_forfait_couleur
                    qte_by_dossier_forfait_noir += k.fleet_forfait_nb
                    qte_by_dossier_abonnement_service += k.fleet_abonnement_service
                    qte_by_dossier_autre += k.fleet_autre
                    qte_by_dossier_sup_coleur += k.couleur_supp
                    qte_by_dossier_sup_noir += k.noir_supp



                if purchase_id:
                    if i[0].augmentation_sav_bool == True:
                        number_of_days = (date.today() - j[1][0].fleet_date_inst).days
                        augmentation = int(number_of_days / 365)
                        taut_augmantation = augmentation * i[0].augmentation_sav
                        cout_copie_coluer = j[0].sale_cout_signe_col + j[0].sale_cout_signe_col * taut_augmantation
                        cout_copie_noir = j[0].sale_cout_signe_nb + j[0].sale_cout_signe_nb * taut_augmantation
                    else:
                        cout_copie_coluer = j[0].sale_cout_signe_col
                        cout_copie_noir = j[0].sale_cout_signe_nb


                    if j[0].sale_forfait_signe_col:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_coleurs.id,
                            'name': j[0].cout_copie_coleurs.name,
                            'price_unit': cout_copie_coluer,
                            'product_uom_qty': j[0].sale_forfait_signe_col,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_forfait_signe_nb:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_noires.id,
                            'name': j[0].cout_copie_noires.name,
                            'price_unit': cout_copie_noir,
                            'product_uom_qty':j[0].sale_forfait_signe_nb ,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if qte_by_dossier_sup_coleur:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_coleurs_sup.id,
                            'name': j[0].cout_copie_coleurs_sup.name,
                            'price_unit': cout_copie_coluer,
                            'product_uom_qty': qte_by_dossier_sup_coleur,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if qte_by_dossier_sup_noir:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_noires_sup.id,
                            'name': j[0].cout_copie_noires_sup.name,
                            'price_unit': cout_copie_noir,
                            'product_uom_qty': qte_by_dossier_sup_noir,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_abonnement_service:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].abonnements.id,
                            'name': j[0].abonnements.name,
                            'price_unit': j[0].sale_abonnement_service,
                            'product_uom_qty': '1',
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_autre_frais:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].services.id,
                            'name': j[0].services.name,
                            'price_unit': j[0].sale_autre_frais,
                            'product_uom_qty': '1',
                        }
                        self.env['sale.order.line'].sudo().create(res)

        #################### tout dossier
        for i in list_client_tout_dossier.items():
            purchase_id = False
            print(i[0].name)
            list_numero_dossier_par_dossier = []
            for j in i[1].items():
                if j[0].sale_dossier not in list_numero_dossier_par_dossier:
                    list_numero_dossier_par_dossier.append(j[0].sale_dossier)
                    if len(list_numero_dossier_par_dossier) <=1:
                        sale_vals = {
                            'company_id': j[0].company_id.id,
                            'date_order': datetime.now(),
                            'partner_id': j[0].partner_id.id,
                            'partner_invoice_id': j[0].partner_invoice_id.id,
                            'partner_shipping_id': j[0].partner_shipping_id.id,
                            'picking_policy': j[0].picking_policy,
                            'pricelist_id': j[0].pricelist_id.id,
                            'warehouse_id': j[0].warehouse_id.id,
                            'state': 'sale',
                            'sale_maintnance': True,
                        }
                        purchase_id1 = self.env['sale.order'].sudo().create(sale_vals)
                        purchase_id = purchase_id1.id
                        print(purchase_id1)
                        print(purchase_id1.sale_maintnance)


                qte_by_dossier_forfait_coleur = 0
                qte_by_dossier_forfait_noir = 0
                qte_by_dossier_sup_coleur = 0
                qte_by_dossier_sup_noir = 0
                qte_by_dossier_abonnement_service = 0
                qte_by_dossier_autre = 0


                for k in j[1]:
                    ######### create devis fleet liste
                    res = {
                        'fleet_id': k.id,
                        'devis_id': purchase_id,
                        'comp_couleur_diff': k.comp_couleur_diff,
                        'comp_noir_diff': k.comp_noir_diff,
                    }
                    id=self.env['listboncommandefleet'].sudo().create(res)




                    qte_by_dossier_forfait_coleur +=  k.fleet_forfait_couleur
                    qte_by_dossier_forfait_noir += k.fleet_forfait_nb
                    qte_by_dossier_abonnement_service += k.fleet_abonnement_service
                    qte_by_dossier_autre += k.fleet_autre
                    qte_by_dossier_sup_coleur += k.couleur_supp
                    qte_by_dossier_sup_noir += k.noir_supp



                res = {
                    'order_id': purchase_id,
                    'display_type': 'line_section',
                    'name': "Dossier N°" + str(j[0].sale_dossier),
                }
                self.env['sale.order.line'].sudo().create(res)


                if purchase_id:
                    if i[0].augmentation_sav_bool == True:
                        number_of_days = (date.today() - j[1][0].fleet_date_inst).days
                        augmentation = int(number_of_days/365)
                        taut_augmantation = augmentation* i[0].augmentation_sav
                        cout_copie_coluer = j[0].sale_cout_signe_col + j[0].sale_cout_signe_col*taut_augmantation
                        cout_copie_noir = j[0].sale_cout_signe_nb + j[0].sale_cout_signe_nb*taut_augmantation
                    else:
                        cout_copie_coluer = j[0].sale_cout_signe_col
                        cout_copie_noir = j[0].sale_cout_signe_nb


                    if j[0].sale_forfait_signe_col:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_coleurs.id,
                            'name': j[0].cout_copie_coleurs.name,
                            'price_unit': cout_copie_coluer,
                            'product_uom_qty': j[0].sale_forfait_signe_col,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_forfait_signe_nb:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_noires.id,
                            'name': j[0].cout_copie_noires.name,
                            'price_unit': cout_copie_noir,
                            'product_uom_qty': j[0].sale_forfait_signe_nb,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if qte_by_dossier_sup_coleur:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_coleurs_sup.id,
                            'name': j[0].cout_copie_coleurs_sup.name,
                            'price_unit': cout_copie_coluer,
                            'product_uom_qty': qte_by_dossier_sup_coleur,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if qte_by_dossier_sup_noir:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_noires_sup.id,
                            'name': j[0].cout_copie_noires_sup.name,
                            'price_unit': cout_copie_noir,
                            'product_uom_qty': qte_by_dossier_sup_noir,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_abonnement_service:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].abonnements.id,
                            'name': j[0].abonnements.name,
                            'price_unit': j[0].sale_abonnement_service,
                            'product_uom_qty': '1',
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_autre_frais:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].services.id,
                            'name': j[0].services.name,
                            'price_unit': j[0].sale_autre_frais,
                            'product_uom_qty': '1',
                        }
                        self.env['sale.order.line'].sudo().create(res)







    ###################### creer facture pour chaque client




class SaleOrderHeritage(models.Model):
    _inherit = 'sale.order'

    devis_a_cree_commande = fields.Boolean(default=False)

    sale_maintnance = fields.Boolean(string="Maintenance", default=False)
    cout_copie_noires = fields.Many2one('product.product', string="Copies noires",
                                        default=lambda self: self.env['product.product'].search([('id', '=', 3)]))
    cout_copie_coleurs = fields.Many2one('product.product', string="Copies couleurs",
                                         default=lambda self: self.env['product.product'].search([('id', '=', 1)]))
    cout_copie_noires_sup = fields.Many2one('product.product', string="Copies noires supplémentaires",
                                            default=lambda self: self.env['product.product'].search([('id', '=', 4)]))
    cout_copie_coleurs_sup = fields.Many2one('product.product', string="Copies couleurs supplémentaires",
                                             default=lambda self: self.env['product.product'].search([('id', '=', 2)]))
    services = fields.Many2one('product.product', string="Services",
                               default=lambda self: self.env['product.product'].search([('id', '=', 6)]))
    abonnements = fields.Many2one('product.product', string="Montant abonnement",
                                             default=lambda self: self.env['product.product'].search([('id', '=', 5)]))
    Frais_livraison = fields.Many2one('product.product', string="Frais d'installation",
                                  default=lambda self: self.env['product.product'].search([('id', '=', 7)]))

    sale_commande_fleet_ids = fields.One2many('listboncommandefleet', inverse_name='devis_id', string="Matériels bon de commande")







class PartnerInherit(models.Model):
    _inherit = 'res.partner'
    type_facture = fields.Selection([('par_dossier', 'facture par dossier'),('tout_dossiers', 'facturer tout les dossiers')],default='par_dossier')

#add field periodicité
class FleetEtatINHERIT(models.Model):
    _inherit = 'fleet.vehicle'
    etat_serie = fields.Selection([('a_jour', 'à facturer'),('n_ajour', 'ne pas facturer')],default='n_ajour')


