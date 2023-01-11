from odoo import models, fields, api


class StockHerit(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('delivery', 'Bon de livraison'), ('done',)])
    delivery_sign = fields.Binary('Signature')
    stock_block_1 = fields.Selection([('Normale', 'Normale'), ('Impaye', 'Impayé')],string="Statut de bon livraison",related="partner_id.x_studio_statut_de_compte")
                                  
    stock_block_yes_1 = fields.Selection([('Normale', 'Normale'), ('Impaye', 'Impayé')],string="Statut de bon livraison ok", compute="get_statu_compute_partner_1")
   
    @api.depends("stock_block_1")
    def get_statu_compute_partner_1(self):
        for rec in self:
            if rec.picking_type_id.id == 2:
                rec.stock_block_yes_1 = rec.stock_block_1
            else:
                rec.stock_block_yes_1 = 'Normale'


    def print_delivery(self):
        if self.state != "done":
            self.write({'state': "delivery"})
        return self.env.ref('stock.action_report_delivery').report_action(self)

    def print_reprise(self):
        return self.env.ref('stock.action_report_delivery').report_action(self)
