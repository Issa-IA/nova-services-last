from odoo import models, fields, api



class serielnumberbyarticle(models.Model):
    _name = 'serielnumber'
    _description = 'Creat serielnumber Auto'
    name = fields.Char(string='Numéros')
    listofseriel1 = fields.Many2one('listofserielnumber', string='les numéros de série')
    listofserielorderline = fields.Many2one('sale.order.line', string='les numéros de série')
    cocher         =  fields.Boolean(string="Cocher")
    def create_serial_fin(self):
        pass

class Listserielnumber(models.Model):
    _name = 'listofserielnumber'
    _description = 'Creat serielnumber Auto'
    product_id = fields.Many2one('product.product', string='Matériel', compute="productcompute")
    sale_order_line = fields.Many2one('sale.order.line', string='sale order line')
    list_serial_number = fields.One2many('serielnumber', string="Numéros de série", inverse_name='listofseriel1')


    def create_serial(self):
        self.sale_order_line.list_serial_number = self.list_serial_number
        list_ok = []
        for rec in self.list_serial_number:
            if rec.cocher == True:
                list_ok.append(rec)
        if len(list_ok) == 1 and self.sale_order_line.product_uom_qty == 1:
            self.sale_order_line.order_line_serie = list_ok[0].name


    @api.depends("sale_order_line")
    def productcompute(self):
        if self.sale_order_line:
            self.product_id = self.sale_order_line.product_id
        else:
            self.product_id =  False


class SaleOrderLineHeritButton(models.Model):
    _inherit    = 'sale.order.line'
    list_serial_number = fields.One2many('serielnumber', string="Numéros de série", inverse_name='listofserielorderline')



    def action_open_listSerial(self):

        print("list of serial", self.product_id)
        vals = {'sale_order_line': self.id, }
        # self.location_dest_id.id
        new_list_seriel = self.env['listofserielnumber'].create(vals)
        list1            =  self.env['stock.production.lot'].search([("product_id","=",self.product_id.id)])
        list =[]
        for num in list1:
            if num.product_qty:
                list.append(num)
        for serial in list:
            self.env['serielnumber'].create(
                {'name': serial.name,
                 'listofseriel1': new_list_seriel.id,

                 })

        return {
                'type': 'ir.actions.act_window',
                'name': 'Choisir les numéros de série',
                'res_model': 'listofserielnumber',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'res_id': new_list_seriel.id,

            }







