from odoo import _, api, fields, models

class Stockpikingheritst(models.Model):
    _inherit    = 'stock.picking'
    id_type_fait = fields.Integer("Preté")
    id_origin_fait = fields.Integer("origin integer", compute="copute_origin")

    def button_validate(self):
        res = super(Stockpikingheritst, self).button_validate()
        for rec in self:
            if rec.picking_type_id.id == 8:
                rec.id_type_fait = 1
        return res
    
    @api.depends('origin')
    def copute_origin(self):
        for rec in self:
            if rec.origin:
                rec.id_origin_fait = 1
                name = rec.origin
                source_doc = name.split()
                name_pret = False
                try:
                    name_pret = source_doc[2]
                except:
                    pass
                if name_pret:
                     sp_stock = self.env['stock.picking'].search([('name', '=', name_pret)])
                     for rec in sp_stock:
                            rec.id_type_fait = 0
            else:
               rec.id_origin_fait = 0 
                
                      
            
   







class Stocktypeinherit(models.Model):
    _inherit    = 'stock.picking.type'
    count_picking_done = fields.Integer(compute='_compute_picking_count_done')
    id_type            = fields.Integer(compute='_id_compute')


    def _id_compute(self):
        for rec in self:
            rec.id_type = rec.id

    def _compute_picking_count_done(self):
        for rec in self:
            fact_count = self.env['stock.picking'].search_count(
                [('id_type_fait', '=',1),('picking_type_id', '=',8)])
            rec.count_picking_done = fact_count
            print("rec.count_picking_done",rec.count_picking_done)

    def open_action_fact(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Les Prêts',
            'res_model': 'stock.picking',
            'view_type': 'form',
            'domain': [ ('id_type_fait', '=',1),('picking_type_id', '=',8)],
            'view_mode': 'tree,form',

        }
