from odoo import models, fields, api
from datetime import date, datetime, timedelta


class SaleMoveHeritfacturation(models.Model):
    _inherit = 'sale.order'

    def curfirstfact(self):
        sale_facture_date= self.env['sale.order'].search([('sale_park','=',True)])
        print(sale_facture_date)
        for sale_fact in sale_facture_date:
            if sale_fact.sale_date_de_debut_contrat:
                    if sale_fact.sale_date_de_debut_contrat >= date.today():
                        sale_orders = self.env['sale.order'].search([('sale_first_bon', '=', True), ('invoice_status', '=', 'to invoice')])
                        invoice_lines = []
                        for sale in sale_orders:
                            if sale.sale_connect:
                                if sale.sale_connect.id == sale_fact.id:
                                    for line in sale.order_line:
                                        if line.display_type:
                                            vals = {
                                                'name': line.name,
                                                'display_type': line.display_type,
                                            }
                                            invoice_lines.append((0, 0, vals))
                                        else:
                                            vals = {
                                                'name': line.name,
                                                'price_unit': line.price_unit,
                                                'quantity': line.product_uom_qty,
                                                'product_id': line.product_id.id,
                                                'product_uom_id': line.product_uom.id,
                                                'sale_line_ids': [(6, 0, [line.id])],
                                            }
                                            invoice_lines.append((0, 0, vals))
                                    self.env['account.move'].create({
                                        'ref': sale.client_order_ref,
                                        'move_type': 'out_invoice',
                                        'invoice_origin': sale.name,
                                        'invoice_user_id': sale.user_id.id,
                                        'partner_id': sale.partner_invoice_id.id,
                                        'invoice_line_ids': invoice_lines,
                                        'acount_maintnance': True,
                                    })
                                    sale.invoice_status = 'invoiced'


