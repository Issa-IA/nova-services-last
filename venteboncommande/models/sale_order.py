from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def create_so(self, sale_order_id):
        sale_vals = {
            'company_id': sale_order_id.company_id.id,
            'date_order': datetime.now(),
            'partner_id': sale_order_id.partner_id.id,
            'partner_invoice_id': sale_order_id.partner_invoice_id.id,
            'partner_shipping_id': sale_order_id.partner_shipping_id.id,
            'picking_policy': sale_order_id.picking_policy,
            'pricelist_id': sale_order_id.pricelist_id.id,
            'warehouse_id':sale_order_id.warehouse_id.id,
            'state': 'sale',
            'sale_maintnance': True,
            'sale_not_update_bon_commande': True,
            'sale_connect':sale_order_id.id,
            'sale_bon_facture_ok':False,
        }

        new_sale_order = self.env['sale.order'].create(sale_vals)
        new_sale_order_id: int = new_sale_order.id
        res = {
            'order_id': new_sale_order_id,
            'display_type': 'line_section',
            'name': "Dossier N°" + str(sale_order_id.sale_dossier),
        }
        self.env['sale.order.line'].create(res)
        cout_copie_coluer = sale_order_id.sale_cout_actuel_col
        cout_copie_noir = sale_order_id.sale_cout_actuel_nb
        
        if sale_order_id.sale_forfait_actuel_col:
            res = {
                'tax_id':sale_order_id.cout_copie_coleurs.taxes_id,
                'order_id': new_sale_order_id,
                'product_id': sale_order_id.cout_copie_coleurs.id,
                'name': sale_order_id.cout_copie_coleurs.name,
                'price_unit': cout_copie_coluer,
                'product_uom_qty': sale_order_id.sale_forfait_actuel_col,
            }
            self.env['sale.order.line'].create(res)

        if sale_order_id.sale_forfait_actuel_nb:
            res = {
                'tax_id':sale_order_id.cout_copie_noires.taxes_id,
                'order_id': new_sale_order_id,
                'product_id': sale_order_id.cout_copie_noires.id,
                'name': sale_order_id.cout_copie_noires.name,
                'price_unit': cout_copie_noir,
                'product_uom_qty': sale_order_id.sale_forfait_actuel_nb,
            }
            self.env['sale.order.line'].create(res)

        if sale_order_id.sale_abonnement_service:
            res = {
                'tax_id':sale_order_id.abonnements.taxes_id,
                'order_id': new_sale_order_id,
                'product_id': sale_order_id.abonnements.id,
                'name': sale_order_id.abonnements.name,
                'price_unit': sale_order_id.sale_abonnement_service_actuel,
                'product_uom_qty': '1',
            }
            self.env['sale.order.line'].create(res)

        if sale_order_id.sale_autre_frais:
            res = {
                'tax_id':sale_order_id.services.taxes_id,
                'order_id': new_sale_order_id,
                'product_id': sale_order_id.services.id,
                'name': sale_order_id.services.name,
                'price_unit': sale_order_id.sale_autre_frais,
                'product_uom_qty': '1',
            }
            self.env['sale.order.line'].create(res)

        if sale_order_id.sale_loyer_fact:
            res = {
                'tax_id':sale_order_id.Frais_loyer.taxes_id,
                'order_id': new_sale_order_id,
                'product_id': sale_order_id.Frais_loyer.id,
                'name': sale_order_id.Frais_loyer.name,
                'price_unit': sale_order_id.sale_loyer_fact,
                'product_uom_qty': '1',
            }
            self.env['sale.order.line'].create(res)
            
        if sale_order_id.sale_pfr_fournissuer:
            res = {
                'tax_id':sale_order_id.pfr_fournisseur.taxes_id,
                'order_id': new_sale_order_id,
                'product_id': sale_order_id.pfr_fournisseur.id,
                'name': sale_order_id.pfr_fournisseur.name,
                'price_unit': sale_order_id.sale_pfr_fournissuer,
                'product_uom_qty': '1',
            }
            self.env['sale.order.line'].create(res)
        sale_order_id.devis_a_cree_commande = False

    @api.model
    def create_sale_orders(self, force_trigger=False):
        today = fields.Date.context_today(self)
        threshold = today + relativedelta(days=1) - relativedelta(years=1)

        sale_order_ids =  self.env['sale.order'].search([
            ('sale_park', '=', True),
            ('company_id', '=', self.env.company.id),
            ('date_last_cout_update_vrai', '!=', False),
            ('date_last_cout_update_vrai', '<=', threshold),
        ])
        for sale_order_id in sale_order_ids:
            sale_order_id.sale_cout_actuel_nb = sale_order_id.sale_cout_actuel_nb + sale_order_id.sale_cout_actuel_nb*sale_order_id.partner_id.augmentation_sav
            sale_order_id.sale_cout_actuel_col = sale_order_id.sale_cout_actuel_col + sale_order_id.sale_cout_actuel_col*sale_order_id.partner_id.augmentation_sav
            sale_order_id.date_last_cout_update_vrai = sale_order_id.date_last_cout_update_vrai + relativedelta(years=1)
        
        sale_order_ids =  self.env['sale.order'].search([
            ('sale_park','=',True), 
            ('company_id','=',self.env.company.id),
            ('sale_date_de_fin_contrat','!=',False),
            ('sale_date_Facture','!=',False),
            ('sale_periode','in',[1,3]),
            ('devis_a_cree_commande','=',True),
        ])

        for sale_order_id in sale_order_ids:
            sale_date_facture = sale_order_id.sale_date_Facture + relativedelta(months=sale_order_id.sale_periode)-relativedelta(days=1)
            if sale_date_facture <= date.today() and sale_order_id.sale_date_Facture <=sale_order_id.sale_date_de_fin_contrat:
                self.create_so(sale_order_id)
