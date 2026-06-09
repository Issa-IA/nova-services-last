from odoo import models, fields

class AccountmoveHeritfacture(models.Model):
    _inherit = 'account.move'
    move_sale_order = fields.Many2one('sale.order', string="Bon de retour")
    account_bonretour = fields.One2many('bonretour', string="Bon de retour", inverse_name='bonretour_stock_move')
    acount_retour = fields.Boolean(default=False)