from odoo import models, fields, api,_
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class StockHeritpicking(models.Model):
    _inherit = 'stock.picking'

    def write(self, values):
        res = super(StockHeritpicking, self).write(values)
        # here you can do accordingly
        return self.update_numero_serie()

    def update_numero_serie(self):
        if self.state == 'done':
            if self.sale_id:
                for record in self.move_line_ids_without_package:
                    list_fleet = self.env['fleet.vehicle'].search([("fleet_devis_id", "=", self.sale_id.id),("fleet_artic_id","=",record.product_id.id)])
                    list_fleet_numero_serie = []
                    for fleet in list_fleet:
                        if fleet.fleet_serie != "False":
                            list_fleet_numero_serie.append(fleet.fleet_serie)
                    for fleet in list_fleet:
                        if fleet.fleet_serie == "False" and (record.lot_id.name not in list_fleet_numero_serie):
                            fleet.fleet_serie = record.lot_id.name
                            break
                    for line in self.sale_id.order_line:
                        if line.product_id.id == record.product_id.id and line.product_uom_qty == 1:
                            line.order_line_serie = record.lot_id.name 
                            break



class CreatParkWizard(models.Model):
    _name = 'creatpark'
    _description = 'Creat Park Auto wizard'
    devis_dossier = fields.Many2one( "sale.order",string='Numéro de dossier')

    def create_parck(self):
        if self.devis_dossier:
            self.devis_dossier.sale_date_Facture = date.today()
            self.devis_dossier.sale_park = True
            if self.devis_dossier.sale_periodicite == 'mens':
                self.devis_dossier.sale_periode = 1
            if self.devis_dossier.sale_periodicite == 'trim':
                self.devis_dossier.sale_periode = 3
            first_devis = False
            for rec in self.devis_dossier.order_line:
                if rec.product_id.parc_ok == True:
                    first_devis = True
                    break
            if first_devis:
                sale_vals = {
                    'company_id': self.devis_dossier.company_id.id,
                    'date_order': datetime.now(),
                    'partner_id': self.devis_dossier.partner_id.id,
                    'partner_invoice_id':self.devis_dossier.partner_invoice_id.id,
                    'partner_shipping_id':self.devis_dossier.partner_shipping_id.id,
                    'picking_policy': self.devis_dossier.picking_policy,
                    'pricelist_id': self.devis_dossier.pricelist_id.id,
                    'warehouse_id': self.devis_dossier.warehouse_id.id,
                    'state': 'sale',
                    'sale_maintnance': True,
                    'sale_connect':self.devis_dossier.id,
                    'sale_first_bon':True,
                }
                purchase_id1 = self.env['sale.order'].sudo().create(sale_vals)
                purchase_id = purchase_id1.id
                res = {
                    'order_id': purchase_id,
                    'display_type': 'line_section',
                    'name': "Dossier N°" + str(self.devis_dossier.sale_dossier),
                }
                self.env['sale.order.line'].sudo().create(res)
                if self.devis_dossier.sale_forfait_signe_col:
                    res = {
                        'order_id': purchase_id,
                        'product_id': self.devis_dossier.cout_copie_coleurs.id,
                        'name': self.devis_dossier.cout_copie_coleurs.name,
                        'price_unit': self.devis_dossier.sale_cout_signe_col,
                        'product_uom_qty': self.devis_dossier.sale_forfait_signe_col,
                    }
                    self.env['sale.order.line'].sudo().create(res)

                if self.devis_dossier.sale_forfait_signe_nb:
                    res = {
                        'order_id': purchase_id,
                        'product_id': self.devis_dossier.cout_copie_noires.id,
                        'name': self.devis_dossier.cout_copie_noires.name,
                        'price_unit': self.devis_dossier.sale_cout_signe_nb,
                        'product_uom_qty': self.devis_dossier.sale_forfait_signe_nb,
                    }
                    self.env['sale.order.line'].sudo().create(res)
                if self.devis_dossier.sale_abonnement_service:
                    res = {
                        'order_id': purchase_id,
                        'product_id': self.devis_dossier.abonnements.id,
                        'name': self.devis_dossier.abonnements.name,
                        'price_unit': self.devis_dossier.sale_abonnement_service,
                        'product_uom_qty': '1',
                    }
                    self.env['sale.order.line'].sudo().create(res)

                if self.devis_dossier.sale_autre_frais:
                    res = {
                        'order_id': purchase_id,
                        'product_id': self.devis_dossier.services.id,
                        'name': self.devis_dossier.services.name,
                        'price_unit': self.devis_dossier.sale_autre_frais,
                        'product_uom_qty': '1',
                    }
                    self.env['sale.order.line'].sudo().create(res)
                if self.devis_dossier.sale_frais:
                    res = {
                        'order_id': purchase_id,
                        'product_id': self.devis_dossier.Frais_livraison.id,
                        'name': self.devis_dossier.Frais_livraison.name,
                        'price_unit': self.devis_dossier.sale_frais,
                        'product_uom_qty': '1',
                    }
                    self.env['sale.order.line'].sudo().create(res)
              
        if self.devis_dossier.order_line:
            if self.devis_dossier.sale_periodicite == 'mens':
                if self.devis_dossier.sale_duree:
                    if self.devis_dossier.sale_duree > 0:
                        expiration_date = date.today() + relativedelta(
                            months=self.devis_dossier.sale_duree) - relativedelta(days=1)
                    else:
                        expiration_date = date.today()
                else:
                    expiration_date = False


            elif self.devis_dossier.sale_periodicite == 'trim':
                if self.devis_dossier.sale_duree:
                    if self.devis_dossier.sale_duree > 0:
                        expiration_date = date.today() + relativedelta(
                            months=(self.devis_dossier.sale_duree * 3)) - relativedelta(days=1)
                    else:
                        expiration_date = date.today()
                else:
                    expiration_date = False

            else:
                expiration_date = False
            self.devis_dossier.sale_date_de_fin_contrat = expiration_date


            for rec in self.devis_dossier.order_line:
                 list_numer_serie = []
                 list_lot_id = []
                 for num in rec.list_serial_number:
                     if num.cocher == True:
                         list_numer_serie.append(num.name)
                         lot_id = self.env['stock.production.lot'].search([("product_id", "=", rec.product_id.id), ("name", "=", num.name)])
                         list_lot_id.append(lot_id)
                 if list_lot_id:
                     list_record = []
                     for record in self.devis_dossier.picking_ids.move_line_ids_without_package:
                         if record.product_id.id == rec.product_id.id:
                             list_record.append(record)

                     compteur = 0
                     for lot_id_num in list_lot_id:
                         if len(list_record) >= compteur+ 1:
                             list_record[compteur].update({'lot_id': lot_id_num.id, 'qty_done': 1, })
                             compteur +=1
                     print("list_lot_id", list_lot_id)
                     print("list_record", list_record)           
                 print(list_numer_serie)
                

                 if rec.product_id.parc_ok:
                     if self.devis_dossier.sale_leaser:
                         sale_leaser = self.devis_dossier.sale_leaser.id
                     else:
                         sale_leaser = False
                    
                     if len(list_numer_serie)< int(rec.product_uom_qty):    
                        for i in range(int(rec.product_uom_qty)-len(list_numer_serie)):
                            list_numer_serie.append('False')
                     
                     for number in range(0, int(rec.product_uom_qty)):
                            vals = {
                                 'fleet_serie': list_numer_serie[number],
                                 'fleet_fournisseur': 8,
                                 'fleet_marque': rec.product_id.product_marque.id,
                                 'fleet_Modele': rec.product_id.product_Modele.id,
                                 'fleet_type_1': rec.product_id.product_type,
                                 'partner_id': self.devis_dossier.partner_id.id,
                                 'fleet_artic_id': rec.product_id.id,
                                 'fleet_expiration_date': expiration_date,
                                 'fleet_type': self.devis_dossier.sale_type,
                                 'fleet_periodicite': self.devis_dossier.sale_periodicite,
                                 'fleet_facturation': self.devis_dossier.sale_periodicite,
                                 'fleet_prix_HT': self.devis_dossier.sale_loyer,
                                 'fleet_duree': self.devis_dossier.sale_duree,
                                 'fleet_leaser': sale_leaser,
                                 'fleet_accord': self.devis_dossier.sale_accord,
                                 'fleet_cout_Couleur': self.devis_dossier.sale_cout_signe_col,
                                 'fleet_forfait_couleur': self.devis_dossier.sale_forfait_signe_col,
                                 'fleet_cout_nb': self.devis_dossier.sale_cout_signe_nb,
                                 'fleet_forfait_nb': self.devis_dossier.sale_forfait_signe_nb,
                                 'fleet_abonnement_service': self.devis_dossier.sale_abonnement_service,
                                 'fleet_autre': self.devis_dossier.sale_autre_frais,
                                 'fleet_partenariat': self.devis_dossier.sale_partenariat,
                                 'fleet_solde_fois': self.devis_dossier.sale_solde_2_fois,
                                 'fleet_date_fin_F': self.devis_dossier.sale_date_fin_F,
                                 'fleet_date_2_solde': self.devis_dossier.sale_date_2_solde,
                                 'fleet_date_inst': date.today(),
                                 'fleet_dossier_devis': self.devis_dossier.sale_dossier,
                                 'fleet_user_id': self.devis_dossier.user_id.id,
                                 'fleet_devis_id': self.devis_dossier.id,}
                            parc_id1 = self.env['fleet.vehicle'].create(vals)
                            vals = {
                                 'num_serie': list_numer_serie[number],
                                 'client_id': self.devis_dossier.partner_id.id,
                                 'fleet_id': parc_id1.id,
                                 'article_id': rec.product_id.id, }
                            self.env['fleetserielarticle'].create(vals)






