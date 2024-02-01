from odoo import models, fields, api


class SaleStateHerit(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('invoiced', 'Facturé')])

    # @api.onchange('invoice_count')
    # def update_state(self):
    #     for rec in self:
    #         if rec.state == 'done':
    #             if rec.invoice_count > 0:
    #                 rec.state = 'invoiced'
                

    def write(self, vals):        
        for rec in self:  
            if rec.state == 'done':
                if rec.invoice_count > 0 :                
                        vals.update({'state':'invoiced'})   
            if rec.state == 'invoiced':
                 if rec.invoice_count = 0 :
                        vals.update({'state':'done'})
        res=super(SaleStateHerit, self).write(vals)
        return res
