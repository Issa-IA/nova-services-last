from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

class SaleMoveHeritbondecommande(models.Model):
    _inherit = 'sale.order'
    def curboncommande(self):
        sale_a_cree_bon_commande =  self.env['sale.order'].search([('sale_park','=',True)])
        for sale_bon_commande in sale_a_cree_bon_commande:
            if sale_bon_commande.sale_date_de_fin_contrat:
                if sale_bon_commande.sale_date_Facture:
                    if sale_bon_commande.sale_periode:
                        if sale_bon_commande.sale_periode == 1:
                            if sale_bon_commande.sale_date_Facture + relativedelta(months=1) <= date.today()+relativedelta(days=1) and sale_bon_commande.sale_date_Facture <=sale_bon_commande.sale_date_de_fin_contrat:
                                if sale_bon_commande.devis_a_cree_commande == True:
                                    sale_vals = {
                                        'company_id': sale_bon_commande.company_id.id,
                                        'date_order': datetime.now(),
                                        'partner_id': sale_bon_commande.partner_id.id,
                                        'partner_invoice_id': sale_bon_commande.partner_invoice_id.id,
                                        'partner_shipping_id': sale_bon_commande.partner_shipping_id.id,
                                        'picking_policy': sale_bon_commande.picking_policy,
                                        'pricelist_id': sale_bon_commande.pricelist_id.id,
                                        'warehouse_id':sale_bon_commande.warehouse_id.id,
                                        'state': 'sale',
                                        'sale_maintnance': True,
                                        'sale_not_update_bon_commande': True,
                                    }
                                    purchase_id1 = self.env['sale.order'].sudo().create(sale_vals)
                                    purchase_id = purchase_id1.id
                                    res = {
                                        'order_id': purchase_id,
                                        'display_type': 'line_section',
                                        'name': "Dossier N°" + str(sale_bon_commande.sale_dossier),
                                    }
                                    self.env['sale.order.line'].sudo().create(res)
                                    if sale_bon_commande.partner_id.augmentation_sav_bool == True:
                                        date_inst = date.today()
                                        for fleet in sale_bon_commande.sale_parc_ids:
                                            if fleet.fleet_date_inst:
                                                date_inst = fleet.fleet_date_inst
                                        number_of_days = (date.today() - date_inst).days
                                        augmentation = int(number_of_days / 365)
                                        taut_augmantation = augmentation * sale_bon_commande.partner_id.augmentation_sav
                                        cout_copie_coluer = sale_bon_commande.sale_cout_signe_col + sale_bon_commande.sale_cout_signe_col * taut_augmantation
                                        cout_copie_noir = sale_bon_commande.sale_cout_signe_nb + sale_bon_commande.sale_cout_signe_nb * taut_augmantation
                                    else:
                                        cout_copie_coluer = sale_bon_commande.sale_cout_signe_col
                                        cout_copie_noir = sale_bon_commande.sale_cout_signe_nb
                                    check = False
                                    if sale_bon_commande.sale_forfait_signe_col:
                                        check = True
                                        res = {
                                            'order_id': purchase_id,
                                            'product_id': sale_bon_commande.cout_copie_coleurs.id,
                                            'name': sale_bon_commande.cout_copie_coleurs.name,
                                            'price_unit': cout_copie_coluer,
                                            'product_uom_qty': sale_bon_commande.sale_forfait_signe_col,
                                        }
                                        self.env['sale.order.line'].sudo().create(res)

                                    if sale_bon_commande.sale_forfait_signe_nb:
                                        check = True
                                        res = {
                                            'order_id': purchase_id,
                                            'product_id': sale_bon_commande.cout_copie_noires.id,
                                            'name': sale_bon_commande.cout_copie_noires.name,
                                            'price_unit': cout_copie_noir,
                                            'product_uom_qty': sale_bon_commande.sale_forfait_signe_nb,
                                        }
                                        self.env['sale.order.line'].sudo().create(res)

                                    if check ==  False:

                                        res = {
                                                'order_id': purchase_id,
                                                'product_id': sale_bon_commande.cout_copie_coleurs_sup.id,
                                                'name': sale_bon_commande.cout_copie_coleurs_sup.name,
                                                'price_unit': cout_copie_coluer,
                                                'product_uom_qty': 0,
                                        }
                                        self.env['sale.order.line'].sudo().create(res)


                                        res = {
                                                'order_id': purchase_id,
                                                'product_id': sale_bon_commande.cout_copie_noires_sup.id,
                                                'name': sale_bon_commande.cout_copie_noires_sup.name,
                                                'price_unit': cout_copie_noir,
                                                'product_uom_qty': 0,
                                        }
                                        self.env['sale.order.line'].sudo().create(res)

                                    if check:

                                        if sale_bon_commande.sale_abonnement_service:
                                            res = {
                                                'order_id': purchase_id,
                                                'product_id': sale_bon_commande.abonnements.id,
                                                'name': sale_bon_commande.abonnements.name,
                                                'price_unit': sale_bon_commande.sale_abonnement_service,
                                                'product_uom_qty': '1',
                                            }
                                            self.env['sale.order.line'].sudo().create(res)

                                        if sale_bon_commande.sale_autre_frais:
                                            res = {
                                                'order_id': purchase_id,
                                                'product_id': sale_bon_commande.services.id,
                                                'name': sale_bon_commande.services.name,
                                                'price_unit': sale_bon_commande.sale_autre_frais,
                                                'product_uom_qty': '1',
                                            }
                                            self.env['sale.order.line'].sudo().create(res)
                        if sale_bon_commande.sale_periode == 3:
                            if sale_bon_commande.sale_date_Facture + relativedelta(months=3) <= date.today()+relativedelta(days=1) and sale_bon_commande.sale_date_Facture <=sale_bon_commande.sale_date_de_fin_contrat:
                                if sale_bon_commande.devis_a_cree_commande == True:
                                    sale_vals = {
                                        'company_id': sale_bon_commande.company_id.id,
                                        'date_order': datetime.now(),
                                        'partner_id': sale_bon_commande.partner_id.id,
                                        'partner_invoice_id': sale_bon_commande.partner_invoice_id.id,
                                        'partner_shipping_id': sale_bon_commande.partner_shipping_id.id,
                                        'picking_policy': sale_bon_commande.picking_policy,
                                        'pricelist_id': sale_bon_commande.pricelist_id.id,
                                        'warehouse_id':sale_bon_commande.warehouse_id.id,
                                        'state': 'sale',
                                        'sale_maintnance': True,
                                        'sale_not_update_bon_commande': True,
                                    }
                                    purchase_id1 = self.env['sale.order'].sudo().create(sale_vals)
                                    purchase_id = purchase_id1.id
                                    res = {
                                        'order_id': purchase_id,
                                        'display_type': 'line_section',
                                        'name': "Dossier N°" + str(sale_bon_commande.sale_dossier),
                                    }
                                    self.env['sale.order.line'].sudo().create(res)
                                    if sale_bon_commande.partner_id.augmentation_sav_bool == True:
                                        date_inst = date.today()
                                        for fleet in sale_bon_commande.sale_parc_ids:
                                            if fleet.fleet_date_inst:
                                                date_inst = fleet.fleet_date_inst
                                        number_of_days = (date.today() - date_inst).days
                                        augmentation = int(number_of_days / 365)
                                        taut_augmantation = augmentation * sale_bon_commande.partner_id.augmentation_sav
                                        cout_copie_coluer = sale_bon_commande.sale_cout_signe_col + sale_bon_commande.sale_cout_signe_col * taut_augmantation
                                        cout_copie_noir = sale_bon_commande.sale_cout_signe_nb + sale_bon_commande.sale_cout_signe_nb * taut_augmantation
                                    else:
                                        cout_copie_coluer = sale_bon_commande.sale_cout_signe_col
                                        cout_copie_noir = sale_bon_commande.sale_cout_signe_nb
                                    check = False
                                    if sale_bon_commande.sale_forfait_signe_col:
                                        check = True
                                        res = {
                                            'order_id': purchase_id,
                                            'product_id': sale_bon_commande.cout_copie_coleurs.id,
                                            'name': sale_bon_commande.cout_copie_coleurs.name,
                                            'price_unit': cout_copie_coluer,
                                            'product_uom_qty': sale_bon_commande.sale_forfait_signe_col,
                                        }
                                        self.env['sale.order.line'].sudo().create(res)

                                    if sale_bon_commande.sale_forfait_signe_nb:
                                        check = True
                                        res = {
                                            'order_id': purchase_id,
                                            'product_id': sale_bon_commande.cout_copie_noires.id,
                                            'name': sale_bon_commande.cout_copie_noires.name,
                                            'price_unit': cout_copie_noir,
                                            'product_uom_qty': sale_bon_commande.sale_forfait_signe_nb,
                                        }
                                        self.env['sale.order.line'].sudo().create(res)

                                    if check ==  False:

                                        res = {
                                                'order_id': purchase_id,
                                                'product_id': sale_bon_commande.cout_copie_coleurs_sup.id,
                                                'name': sale_bon_commande.cout_copie_coleurs_sup.name,
                                                'price_unit': cout_copie_coluer,
                                                'product_uom_qty': 0,
                                        }
                                        self.env['sale.order.line'].sudo().create(res)


                                        res = {
                                                'order_id': purchase_id,
                                                'product_id': sale_bon_commande.cout_copie_noires_sup.id,
                                                'name': sale_bon_commande.cout_copie_noires_sup.name,
                                                'price_unit': cout_copie_noir,
                                                'product_uom_qty': 0,
                                        }
                                        self.env['sale.order.line'].sudo().create(res)

                                    if check:
                                        if sale_bon_commande.sale_abonnement_service:
                                            res = {
                                                'order_id': purchase_id,
                                                'product_id': sale_bon_commande.abonnements.id,
                                                'name': sale_bon_commande.abonnements.name,
                                                'price_unit': sale_bon_commande.sale_abonnement_service,
                                                'product_uom_qty': '1',
                                            }
                                            self.env['sale.order.line'].sudo().create(res)

                                        if sale_bon_commande.sale_autre_frais:
                                            res = {
                                                'order_id': purchase_id,
                                                'product_id': sale_bon_commande.services.id,
                                                'name': sale_bon_commande.services.name,
                                                'price_unit': sale_bon_commande.sale_autre_frais,
                                                'product_uom_qty': '1',
                                            }
                                            self.env['sale.order.line'].sudo().create(res)








