from odoo import models, fields, api


class SaleStateHerit(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('invoiced', 'Facturé')])

    def write(self, vals):
        for rec in self:  
            if rec.invoice_count > 0 :
                if rec.state == 'done':
                    vals.update({'state':'invoiced'})   
            else:
                if rec.state == 'invoiced':
                    vals.update({'state':'done'})
        res=super(SaleStateHerit, self).write(vals)
        return res
