from odoo import models, api, _
from datetime import date
from dateutil.relativedelta import relativedelta
# from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
class SaleMoveHeritfacture(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create_invoice_from_sale_order(self):
        sale_order_ids = self.env['sale.order'].search([
            ('sale_park','=',True),
            ('company_id','=',self.env.company.id),
            ('sale_date_Facture','!=',False),
            ('sale_periode','in',[1,3]),
        ])

        total_invoices: int = 0
        sale_orders_to_invoice_ids = self.env['sale.order'].search([
            ('company_id','=',self.env.company.id),
            ('sale_maintnance', '=', True),
            ('invoice_status', '=', 'to invoice'),
            ('sale_bon_facture_ok','=', False),
        ])
        for sale_order_id in sale_order_ids:            
            if sale_order_id.sale_periode in [1,3]:
                new_date = sale_order_id.sale_date_Facture + relativedelta(months=sale_order_id.sale_periode)
                if new_date <= date.today():
                    sale_order_id.sale_date_Facture = new_date

                    for so_to_inv_id in sale_orders_to_invoice_ids:
                        linked_by_fleet = (
                            so_to_inv_id.sale_commande_fleet_ids
                            and so_to_inv_id.sale_commande_fleet_ids[0].fleet_id.fleet_devis_id.id == sale_order_id.id
                        )
                        linked_by_connect = (
                            so_to_inv_id.sale_connect
                            and so_to_inv_id.sale_connect.id == sale_order_id.id
                        )
                        if not (linked_by_fleet or linked_by_connect):
                            continue

                        invoice_lines = []
                        existing = self.env['account.move'].search([
                            ('move_type', '=', 'out_invoice'),
                            ('invoice_origin', '=', so_to_inv_id.name),
                            ('acount_maintnance', '=', True),
                        ], limit=1)

                        if existing:
                            so_to_inv_id.invoice_status = 'invoiced'
                            so_to_inv_id.sale_bon_facture_ok = True
                            continue

                        total_invoices += 1

                        for line in so_to_inv_id.order_line:
                            if line.display_type:
                                vals = {
                                    'name': line.name,
                                    'display_type': line.display_type,
                                }
                                invoice_lines.append((0, 0, vals))
                            else:
                                vals = {
                                    'tax_ids': line.tax_id,
                                    'name': line.name,
                                    'price_unit': line.price_unit,
                                    'quantity': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom_id': line.product_uom.id,
                                    'sale_line_ids': [(6, 0, [line.id])],
                                }
                                invoice_lines.append((0, 0, vals))

                        self.env['account.move'].create({
                            'ref': so_to_inv_id.client_order_ref,
                            'move_type': 'out_invoice',
                            'invoice_origin': so_to_inv_id.name,
                            'invoice_user_id': so_to_inv_id.user_id.id,
                            'partner_id': so_to_inv_id.partner_id.id,
                            'invoice_line_ids': invoice_lines,
                            'acount_maintnance': True,
                        })
                        so_to_inv_id.invoice_status = 'invoiced'
                        so_to_inv_id.sale_bon_facture_ok = True

        _logger.info("The invoices have been created successfully. %s invoices have been created.", total_invoices)