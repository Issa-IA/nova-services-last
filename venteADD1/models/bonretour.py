
from odoo import models, fields, api
from datetime import date


class SaleOrderfacture(models.Model):
    _inherit    = 'sale.order'

    sale_account = fields.One2many('account.move', string="Facture", inverse_name='move_sale_order')
    account_count = fields.Integer(string="Facture", compute="compute_fact_count")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)

    def compute_fact_count(self):
        for rec in self:
            rec.account_count = self.env['account.move'].search_count([('move_sale_order', '=', rec.id)])

    def action_open_acount(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture fournisseur',
            'res_model': 'account.move',
            'view_type': 'form',
            'domain': [('move_sale_order', '=', self.id)],
            'view_mode': 'list,form',
            'target': 'current',

        }
    
    def action_confirm(self):
        res = super(SaleOrderfacture, self).action_confirm()
        for rec in self:
            facture_with_ligne = dict()
            for rec in self:
                for retour in rec.sale_bonretour:
                    if retour.bonretour_montant > 0:
                        if retour.bonretour_leaser.partner_id:
                            if retour.bonretour_leaser.partner_id.id not in facture_with_ligne.keys():
                                new_account_move = self.env['account.move'].sudo().create({
                                    'ref': rec.client_order_ref,
                                    'move_type': 'in_invoice',
                                    'invoice_origin': rec.name,
                                    'invoice_user_id': rec.user_id.id,
                                    'partner_id': retour.bonretour_leaser.partner_id.id,
                                    'acount_retour': True,
                                    'move_sale_order': rec.id
                                })
                                id = retour.bonretour_leaser.partner_id.id
                                facture_with_ligne[id] = new_account_move
                
                for retour in rec.sale_bonretour:
                    if retour.bonretour_montant > 0:
                        if retour.bonretour_leaser.partner_id:
                            move = self.env['account.move.line'].sudo().with_context(check_move_validity=False).create({
                                'partner_id': retour.bonretour_leaser.partner_id.id,
                                'name': retour.bonretour_article.name,
                                'product_id': retour.bonretour_article.id,
                                'move_id': facture_with_ligne[retour.bonretour_leaser.partner_id.id].id,
                                'quantity': 1,
                                'move_line_serie': retour.bonretour_serie,
                                'price_unit': retour.bonretour_montant,
                                'product_uom_id': retour.bonretour_article.uom_id.id,
                                'date': date.today(),
                                'tax_ids': retour.bonretour_article.supplier_taxes_id.ids,
                            })

        return res

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
    bonretour_location_id = fields.Many2one('stock.location', 'De')
    bonretour_location_dest_id = fields.Many2one('stock.location', 'Vers')

    bonretour_stock_move = fields.Many2one('stock.move', string="stock move")
    bonretour_recep_ok = fields.Boolean(default=False)

class StockLotReprise(models.Model):
    _inherit = 'stock.lot'
    reprise_montant = fields.Float('Montant reprise', digits='Product Price', default=0.0)


class StockQuantReprise(models.Model):
    _inherit = 'stock.quant'

    @api.depends('lot_id.reprise_montant')
    def _compute_value(self):
        super()._compute_value()
        for quant in self:
            if not quant.lot_id or not quant.location_id:
                continue
            if not quant.location_id._should_be_valued():
                continue
            if quant.lot_id.reprise_montant > 0:
                quant.value = quant.quantity * quant.lot_id.reprise_montant


class StockmoveLineHeritretour(models.Model):
    _inherit = 'stock.move.line'
    acount_retour_serie_line = fields.Char(string="N° serie à retourner")
    
class StockmoveHeritretour(models.Model):
    _inherit = 'stock.move'

    acount_retour_serie = fields.Char(string="N° serie")
    stock_move_bonretour = fields.Many2one('bonretour', string="Bon de retour")

    def write(self, values):
        res = super().write(values)
        return self.create_serienumber()
    
    def create_serienumber(self):
        for record in self:
            if record.lot_ids:
                for rec in record.lot_ids:
                    if record.stock_move_bonretour:
                        record.stock_move_bonretour.update({'bonretour_serie': rec.name, })



class Stockpikingretour(models.Model):
    _inherit    = 'stock.picking'
    
    stock_retour_ok = fields.Boolean(default=False)
    stock_reception_ok = fields.Boolean(default=False)
    
    def button_validate(self):
        for rec in self:
            if rec.stock_retour_ok or rec.stock_reception_ok:
                for ligne in rec.move_ids_without_package:
                    bonretour = ligne.stock_move_bonretour
                    if not bonretour or bonretour.bonretour_montant <= 0:
                        continue
                    # Pour AVCO/FIFO : price_unit est lu par _get_price_unit() lors de la création SVL
                    ligne.price_unit = bonretour.bonretour_montant

        res = super(Stockpikingretour, self).button_validate()

        # Après validation : on écrit reprise_montant sur le lot de chaque mouvement de reprise.
        # _compute_value de stock.quant retourne alors quantity * lot.reprise_montant, ce qui
        # affiche exactement bonretour_montant comme valeur dans la vue des emplacements.
        for rec in self:
            if rec.stock_retour_ok or rec.stock_reception_ok:
                for ligne in rec.move_ids_without_package:
                    bonretour = ligne.stock_move_bonretour
                    if not bonretour or bonretour.bonretour_montant <= 0:
                        continue
                    for ml in ligne.move_line_ids:
                        if ml.lot_id:
                            ml.lot_id.sudo().reprise_montant = bonretour.bonretour_montant

        for rec in self:
            if rec.stock_retour_ok or rec.stock_reception_ok:
                for ligne in rec.move_ids_without_package:
                    lot_id = self.env['stock.lot'].search([('name', '=', ligne.acount_retour_serie)])
                    lot_id.update({'ref': 'Reprise' + ' ' + rec.partner_id.name})

        return res
    
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
            'view_mode': 'list,form',
            'target': 'current',

        }

    sale_bonretour = fields.One2many('bonretour', string="Bon de retour", inverse_name='bonretour_sale_order')
    move_type = fields.Selection(
        [('direct', 'Aussi vite que possible'), ('one', 'Lorsque tous les articles sont prêts')], default='direct')
    procure_method=fields.Selection([('make_to_stock','Par défaut : prendre dans le stock'),('make_to_order',"	Avancé : appliquer les règles d'approvisionnement")], default='make_to_stock')


    def write(self, values):
        res = super().write(values)
        return self.create_stock_piking()

    _BONRETOUR_PICKING_CONFIG = {
        'reception': {'name_prefix': 'Recep', 'flag': 'stock_reception_ok', 'picking_type_index': 0},
        'retour': {'name_prefix': 'Retour', 'flag': 'stock_retour_ok', 'picking_type_index': 3},
    }

    def _bonretour_lot(self, retour):
        return self.env['stock.lot'].search([
            ("product_id", "=", retour.bonretour_article.id),
            ("name", "=", retour.bonretour_serie),
        ])

    def _bonretour_needs_move(self, retour, stock_kind):
        lot = self._bonretour_lot(retour)
        if stock_kind == 'reception':
            return not lot
        return bool(lot) and not retour.bonretour_recep_ok

    def _create_bonretour_move(self, retour, picking, mark_received=False):
        self.ensure_one()
        move = self.env['stock.move'].create({
            'company_id': self.company_id.id,
            'date': date.today(),
            'location_dest_id': retour.bonretour_location_dest_id.id,
            'location_id': retour.bonretour_location_id.id,
            'name': 'new',
            'procure_method': self.procure_method,
            'product_id': retour.bonretour_article.id,
            'product_uom': retour.bonretour_article.uom_id.id,
            'product_uom_qty': 1,
            'picking_id': picking.id,
            'stock_move_bonretour': retour.id,
            'acount_retour_serie': retour.bonretour_serie,
        })
        retour.bonretour_stock_move = move.id
        retour.bonretour_stock_piking = picking.id
        if mark_received:
            retour.bonretour_recep_ok = True
        return move

    def _create_bonretour_picking(self, stock_type, stock_kind):
        self.ensure_one()
        config = self._BONRETOUR_PICKING_CONFIG[stock_kind]
        # Comportement historique conserve : les emplacements du picking sont
        # repris de la derniere ligne du bon de retour.
        last = self.sale_bonretour[-1]
        return self.env['stock.picking'].create({
            'name': '%s %s' % (config['name_prefix'], self.name),
            config['flag']: True,
            'partner_id': self.partner_id.id,
            'move_type': self.move_type,
            'location_dest_id': last.bonretour_location_dest_id.id,
            'location_id': last.bonretour_location_id.id,
            'state': 'assigned',
            'picking_type_id': stock_type[config['picking_type_index']].id,
            'stock_sale': self.id,
            'stock_type': stock_kind,
            'stock_compteur_depart_Nb': '0',
            'stock_compteur_depart_C': '0',
            'stock_compteur_retour_Nb': '0',
            'stock_compteur_retour_C': '0',
        })

    def _process_bonretour_stock(self, stock_type, stock_kind):
        self.ensure_one()
        if not self.sale_bonretour:
            return
        mark_received = stock_kind == 'reception'
        picking = self.env['stock.picking'].search([
            ('stock_sale', '=', self.id),
            ('stock_type', '=', stock_kind),
        ])
        if picking:
            for retour in self.sale_bonretour:
                if self._bonretour_needs_move(retour, stock_kind) and retour not in picking.stock_bonretour:
                    self._create_bonretour_move(retour, picking[0], mark_received=mark_received)
        else:
            to_process = self.sale_bonretour.filtered(
                lambda r: self._bonretour_needs_move(r, stock_kind))
            if not to_process:
                return
            picking = self._create_bonretour_picking(stock_type, stock_kind)
            for retour in to_process:
                self._create_bonretour_move(retour, picking, mark_received=mark_received)

    def create_stock_piking(self):
        stock_type = self.env['stock.picking.type'].search([])
        if len(stock_type) <= 1:
            return
        # 'reception' est entierement traite avant 'retour' : le flag
        # bonretour_recep_ok pose en reception est relu en retour.
        for stock_kind in ('reception', 'retour'):
            for rec in self:
                rec._process_bonretour_stock(stock_type, stock_kind)
