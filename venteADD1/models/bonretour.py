
from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class AccountmoveHeritfacture(models.Model):
    _inherit = 'account.move'
    move_sale_order = fields.Many2one('sale.order', string="Bon de retour")
    account_bonretour = fields.One2many('bonretour', string="Bon de retour", inverse_name='bonretour_stock_move')
    acount_retour = fields.Boolean(default=False)


class SaleOrderfacture(models.Model):
    _inherit    = 'sale.order'
    ########## smart button to stock
    sale_account = fields.One2many('account.move', string="Facture", inverse_name='move_sale_order')
    account_count = fields.Integer(string="Facture", compute="compute_fact_count")

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)


    def compute_fact_count(self):
        for rec in self:
            order_count = self.env['account.move'].search_count([('move_sale_order', '=', rec.id)])
            rec.account_count = order_count


    def action_open_acount(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture fournisseur',
            'res_model': 'account.move',
            'view_type': 'form',
            'domain': [('move_sale_order', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',

        }
    ##############################################
    def write(self, values):
        res = super(SaleOrderfacture, self).write(values)
        # here you can do accordingly
        return self.create_stock_move()

    def create_stock_move(self):

        for rec in self:
                sp_stock = self.env['account.move'].search([('move_sale_order', '=', rec.id)])
                if sp_stock:
                    liste_article =[]
                    for record in  sp_stock:
                        if record.invoice_line_ids:
                            for article in record.invoice_line_ids:
                                liste_article.append(article.product_id.id)
                    for ligne in rec.sale_bonretour:
                            if ligne.bonretour_montant > 0:
                                if ligne.bonretour_article.id not in liste_article:
                                    move=self.env['account.move.line'].sudo().with_context(check_move_validity=False).create({
                                        'partner_id': rec.partner_id.id,
                                        'name': rec.partner_id.name,
                                        'product_id': ligne.bonretour_article.id,
                                        'move_id': sp_stock.id,
                                        'quantity': 1,
                                        'price_unit':ligne.bonretour_montant,
                                        'product_uom_id': ligne.bonretour_article.uom_id.id,
                                        'date': date.today(),
                                        'account_id': rec.partner_id.property_account_payable_id.id,

                                    })
                else:
                    if rec.sale_bonretour:
                        new_account_move_id = 0
                        for retour in rec.sale_bonretour:
                            if retour.bonretour_montant > 0:
                                new_account_move = self.env['account.move'].sudo().create({
                                    'ref': rec.client_order_ref,
                                    'move_type': 'in_invoice',
                                    'invoice_origin': rec.name,
                                    'invoice_user_id': rec.user_id.id,
                                    'partner_id': rec.partner_id.id,
                                    'acount_retour': True,
                                    'move_sale_order': rec.id
                                })
                                new_account_move_id = new_account_move.id
                                print('new_account_move', new_account_move)
                                break


class Bonretourtable(models.Model):
    _name = 'bonretour'
    _description = 'Cree un bon retour'

    bonretour_montant = fields.Float(string="Montant du rachat")
    bonretour_leaser = fields.Many2one("typeleaser", string='Leaser')
    bonretour_dossier  = fields.Char(string="Dossier N°")
    bonretour_date_rachat_prevue = fields.Date("Date de rachat prévue")
    bonretour_article = fields.Many2one('product.product', string="Matériels rachetés")

    bonretour_serie = fields.Char(string="N° serie")
    bonretour_sale_order = fields.Many2one('sale.order', string="Matériels rachetés")
    bonretour_stock_piking = fields.Many2one('stock.picking', string="Matériels rachetés")


    ##########new
    bonretour_stock_move = fields.Many2one('stock.move', string="stock move")

class StockmoveLineHeritretour(models.Model):
    _inherit = 'stock.move.line'
    acount_retour_serie_line = fields.Char(string="N° serie à retourner")
    
class StockmoveHeritretour(models.Model):
    _inherit = 'stock.move'
    acount_retour_serie = fields.Char(string="N° serie")

    ###########new
    stock_move_bonretour = fields.Many2one('bonretour', string="Bon de retour")

    def write(self, values):
        res = super(StockmoveHeritretour, self).write(values)
        # here you can do accordingly
        return self.create_serienumber()
    def create_serienumber(self):
        for record in self:
            if record.lot_ids:
                for rec in record.lot_ids:
                    if record.stock_move_bonretour:
                        record.stock_move_bonretour.update({'bonretour_serie': rec.name, })



class Stockpikingretour(models.Model):
    _inherit    = 'stock.picking'
    stock_sale = fields.Many2one('sale.order', string="Bon de commande de retour")
    stock_bonretour = fields.One2many('bonretour', string="Bon de retour", inverse_name='bonretour_stock_piking')
    stock_type = fields.Selection([('reception', 'reception'), ('retour', 'retour')])
    
    #############blockage livraison    
    stock_block = fields.Selection([('Normale', 'Normale'), ('Impaye', 'Impayé')],string="Statut de bon livraison", related="partner_id.x_studio_statut_de_compte")    
    
    stock_block_yes = fields.Selection([('Normale', 'Normale'), ('Impaye', 'Impayé')],string="Statut de bon livraison ok", compute="get_statu_compute_partner")
   
    @api.depends("stock_block")
    def get_statu_compute_partner(self):
        for rec in self:
            if rec.picking_type_id.id == 2:
                rec.stock_block_yes = rec.stock_block
            else:
                rec.stock_block_yes = 'Normale'
    
    ############## new demande
    stock_type_id = fields.Integer(compute="compute_id_type")
   
    @api.depends("picking_type_id")
    def compute_id_type(self):
        for rec in self:
            rec.stock_type_id=rec.picking_type_id.id
    
    stock_compteur_depart_Nb = fields.Char(string="Compteur de départ NB")
    stock_compteur_depart_C = fields.Char(string="Compteur de départ Couleur")
    stock_compteur_retour_Nb = fields.Char(string="Compteur de retour NB")
    stock_compteur_retour_C = fields.Char(string="Compteur de retour Couleur")
    ################


class SaleOrderbonretour(models.Model):
    _inherit    = 'sale.order'

    ########## smart button to stock
    sale_stock = fields.One2many('stock.picking', string="Bon de retour", inverse_name='stock_sale')
    par_stock_count = fields.Integer(string="Bon de retour", compute="compute_stock_count")

    def compute_stock_count(self):
        for rec in self:
            order_count = self.env['stock.picking'].search_count([('stock_sale', '=', rec.id)])
            rec.par_stock_count = order_count

    def action_open_stock(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reprise',
            'res_model': 'stock.picking',
            'view_type': 'form',
            'domain': [('stock_sale', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',

        }
    ##############################################



    sale_bonretour = fields.One2many('bonretour', string="Bon de retour", inverse_name='bonretour_sale_order')
    move_type = fields.Selection(
        [('direct', 'Aussi vite que possible'), ('one', 'Lorsque tous les articles sont prêts')], default='direct')
    procure_method=fields.Selection([('make_to_stock','Par défaut : prendre dans le stock'),('make_to_order',"	Avancé : appliquer les règles d'approvisionnement")], default='make_to_stock')



    def write(self, values):
        res = super(SaleOrderbonretour, self).write(values)
        # here you can do accordingly
        return self.create_stock_piking()

    def create_stock_piking(self):
        stock_type = self.env['stock.picking.type'].search([])

        for rec in self:
            if len(stock_type) > 1:
                sp_stock = self.env['stock.picking'].search(
                    [('stock_sale', '=', rec.id), (('stock_type', '=', 'reception'))])
                if sp_stock:
                    for retour in rec.sale_bonretour:
                        lot_id = self.env['stock.production.lot'].search(
                            [("product_id", "=", retour.bonretour_article.id),
                             ("name", "=", retour.bonretour_serie)])
                        if not lot_id:
                            if retour not in sp_stock.stock_bonretour:
                                move = self.env['stock.move'].create(
                                    {'company_id': rec.company_id.id,
                                     'date': date.today(),
                                     'location_dest_id': 8,
                                     'location_id': 5,
                                     'name': 'new',
                                     'procure_method': rec.procure_method,
                                     'product_id': retour.bonretour_article.id,
                                     'product_uom': retour.bonretour_article.uom_id.id,
                                     'product_uom_qty': 1,
                                     'picking_id': sp_stock[0].id,
                                     'stock_move_bonretour': retour.id,

                                     'acount_retour_serie': retour.bonretour_serie,
                                     })
                                retour.bonretour_stock_move = move.id
                                retour.bonretour_stock_piking = sp_stock[0].id

                        # sp_stock[0].update({'state': 'assigned', })
                else:
                    if rec.sale_bonretour:
                        list1 = []
                        for retour in rec.sale_bonretour:
                            lot_id = self.env['stock.production.lot'].search(
                                [("product_id", "=", retour.bonretour_article.id),
                                 ("name", "=", retour.bonretour_serie)])
                            if lot_id:
                                list1.append(lot_id)
                        if len(rec.sale_bonretour) > len(list1):

                            vals = {'name': 'Recep'+' '+ str(rec.name),
                                    'partner_id': rec.partner_id.id,
                                    'move_type': rec.move_type,
                                    'location_id': 5,
                                    'location_dest_id': 8,
                                    'state': 'assigned',
                                    'picking_type_id': stock_type[0].id,
                                    'stock_sale': rec.id,
                                    'stock_type': 'reception',
                                    'stock_compteur_depart_Nb':'0',
                                    'stock_compteur_depart_C':'0',
                                    'stock_compteur_retour_Nb':'0',
                                    'stock_compteur_retour_C':'0',

                                    }
                            # self.location_dest_id.id
                            new_reception = self.env['stock.picking'].create(vals)

                            for retour in rec.sale_bonretour:
                                lot_id = self.env['stock.production.lot'].search(
                                    [("product_id", "=", retour.bonretour_article.id),
                                     ("name", "=", retour.bonretour_serie)])
                                if not lot_id:
                                    # product_uom = \
                                    # self.env['product.template'].search_read([('id', '=', retour.bonretour_article.id)])[0]['uom_id'][0]
                                    move_ne = self.env['stock.move'].create(
                                        {'company_id': rec.company_id.id,
                                         'date': date.today(),
                                         'location_dest_id': 8,
                                         'location_id': 5,
                                         'name': 'new',
                                         'procure_method': rec.procure_method,
                                         'product_id': retour.bonretour_article.id,
                                         'product_uom': retour.bonretour_article.uom_id.id,
                                         'product_uom_qty': 1,
                                         'picking_id': new_reception.id,
                                         'acount_retour_serie': retour.bonretour_serie,
                                         'stock_move_bonretour': retour.id,

                                         })

                                    retour.bonretour_stock_move = move_ne.id
                                    retour.bonretour_stock_piking = new_reception.id
                                # new_reception.update({'state': 'assigned', })
        for rec in self:
            if len(stock_type) > 1:
                sp_stock = self.env['stock.picking'].search(
                    [('stock_sale', '=', rec.id), (('stock_type', '=', 'retour'))])
                if sp_stock:
                    for retour in rec.sale_bonretour:
                        lot_id = self.env['stock.production.lot'].search(
                            [("product_id", "=", retour.bonretour_article.id),
                             ("name", "=", retour.bonretour_serie)])
                        if  lot_id:
                            if retour not in sp_stock.stock_bonretour:
                                move = self.env['stock.move'].create(
                                    {'company_id': rec.company_id.id,
                                     'date': date.today(),
                                     'location_dest_id': 8,
                                     'location_id': 5,
                                     'name': 'new',
                                     'procure_method': rec.procure_method,
                                     'product_id': retour.bonretour_article.id,
                                     'product_uom': retour.bonretour_article.uom_id.id,
                                     'product_uom_qty': 1,
                                     'picking_id': sp_stock[0].id,
                                     'stock_move_bonretour': retour.id,

                                     'acount_retour_serie': retour.bonretour_serie,
                                     })
                                retour.bonretour_stock_move = move.id
                                retour.bonretour_stock_piking = sp_stock[0].id

                        # sp_stock[0].update({'state': 'assigned', })
                else:
                    if rec.sale_bonretour:
                        list1 = []
                        for retour in rec.sale_bonretour:
                            lot_id = self.env['stock.production.lot'].search(
                                [("product_id", "=", retour.bonretour_article.id),
                                 ("name", "=", retour.bonretour_serie)])
                            if lot_id:
                                list1.append(lot_id)
                        if list1:

                            vals = {'name': 'Retour'+' '+str(rec.name),
                                    'partner_id': rec.partner_id.id,
                                    'move_type': rec.move_type,
                                    'location_id': 5,
                                    'location_dest_id': 8,
                                    'state': 'assigned',
                                    'picking_type_id': stock_type[3].id,
                                    'stock_sale': rec.id,
                                    'stock_type': 'retour',
                                    'stock_compteur_depart_Nb':'0',
                                    'stock_compteur_depart_C':'0',
                                    'stock_compteur_retour_Nb':'0',
                                    'stock_compteur_retour_C':'0',

                                    }
                            # self.location_dest_id.id
                            new_reception = self.env['stock.picking'].create(vals)

                            for retour in rec.sale_bonretour:
                                lot_id = self.env['stock.production.lot'].search(
                                    [("product_id", "=", retour.bonretour_article.id),
                                     ("name", "=", retour.bonretour_serie)])
                                if  lot_id:
                                    # product_uom = \
                                    # self.env['product.template'].search_read([('id', '=', retour.bonretour_article.id)])[0]['uom_id'][0]
                                    move_ne = self.env['stock.move'].create(
                                        {'company_id': rec.company_id.id,
                                         'date': date.today(),
                                         'location_dest_id': 8,
                                         'location_id': 5,
                                         'name': 'new',
                                         'procure_method': rec.procure_method,
                                         'product_id': retour.bonretour_article.id,
                                         'product_uom': retour.bonretour_article.uom_id.id,
                                         'product_uom_qty': 1,
                                         'picking_id': new_reception.id,
                                         'acount_retour_serie': retour.bonretour_serie,
                                         'stock_move_bonretour': retour.id,

                                         })

                                    retour.bonretour_stock_move = move_ne.id
                                    retour.bonretour_stock_piking = new_reception.id
                                # new_reception.update({'state': 'assigned', })

"""
        self.env['stock.move'].create(
            {'product_uom_qty': self.qte_RMA_tr_1, 'product_id': id_article, 'picking_id': new_reception.id,
             'company_id': self.company_id.id, 'date': datetime.date.today(), 'location_id': loc_id,
             'location_dest_id': des_id, 'procure_method': self.procure_method,
             'name': 'new', 'etat': 'ok',
             'product_uom': product_uom_1
             })
"""
