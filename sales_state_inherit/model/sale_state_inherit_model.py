from odoo import models, fields, api


class SaleStateHerit(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('invoiced', 'Facturé')])

    def write(self, vals):
        if self.invoice_count > 0 :
            vals.update({'state':'invoiced'})
        res=super(SaleStateHerit, self).write(vals)
        return res