from odoo import api, fields, models


class ProductProductInherit(models.Model):
    _inherit = "product.template"
    parc_ok = fields.Boolean(default=False, string="Peut être un Parc")
    #serie_number_materiel = fields.Char(string="N° serie")
    product_marque = fields.Many2one("fleet.vehicle.model.brand", string='Marque', related="product_Modele.brand_id")
    product_Modele = fields.Many2one("fleet.vehicle.model", string='Modèle')
    product_type = fields.Char(string='Type', compute="product_type_compute")
    product_type1 = fields.Char(string='Type', compute="product_type_compute1")
    
    @api.onchange('product_Modele')
    def product_type_compute1(self):
        for rec in self:
            if rec.product_Modele.type_materiels:
                    rec.product_type1 = str(rec.product_Modele.type_materiels)
            else:
                rec.product_type1 = False

    @api.onchange('product_Modele')
    def product_type_compute(self):
        for rec in self:
            if rec.product_Modele.category_id:
                if rec.product_Modele.model_format1:
                    rec.product_type = str(rec.product_Modele.category_id.name) + ' ' + str(rec.product_Modele.model_format1.name)
                else:
                    rec.product_type = str(rec.product_Modele.category_id.name)
            else:
                rec.product_type = False


