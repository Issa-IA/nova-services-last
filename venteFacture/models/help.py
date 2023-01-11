"""
print("Bonjour")
        sale_orders = self.env['sale.order'].search([('sale_maintnance','=',True),('invoice_status','=','to invoice')])
        print(sale_orders)
        invoice_lines = []
        for sale in sale_orders:
            print(sale.partner_id.type_facture )
            print(sale.sale_commande_fleet_ids[0].fleet_id.fleet_devis_id)
            print(sale.sale_commande_fleet_ids[0].fleet_id.fleet_devis_id.sale_periodicite)
            print(sale.sale_commande_fleet_ids[0].fleet_id.fleet_date_inst)
            print(sale.sale_commande_fleet_ids[0].fleet_id.fleet_expiration_date)
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
                'acount_maintnance':True,
            })
            sale.invoice_status = 'invoiced'












"""