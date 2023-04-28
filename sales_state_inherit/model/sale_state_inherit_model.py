from odoo import models, fields, api


class SaleStateHerit(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('invoiced', 'Facturé')])

    def write(self, vals):
        
        if self.invoice_count > 0 :
            if self.state == 'done':
                vals.update({'state':'invoiced'})   
        else:
            if self.state == 'invoiced':
                vals.update({'state':'done'})
        res=super(SaleStateHerit, self).write(vals)
        return res
