from odoo import models, fields, api


class SaleStateHerit(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('invoiced', 'Facturé')])

    def write(self, vals):        
        for rec in self:  
            if rec.state == 'sale':
                if rec.invoice_count > 0 :                
                        vals.update({'state':'invoiced'})   
            if rec.state == 'invoiced':
                 if rec.invoice_count == 0 :
                        vals.update({'state':'sale'})
        res=super(SaleStateHerit, self).write(vals)
        return res
