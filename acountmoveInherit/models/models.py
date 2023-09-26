from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class MoveLineHerit(models.Model):
    _inherit = "account.move.line"
    ############ if one serie numberr
    move_line_serie = fields.Char(string="N° serie")
    ############


class AcountMoveHerit(models.Model):
    _inherit = 'account.move'
    
    fact_anne_ = fields.Integer(string="Année de facturation", compute="_compute_anne_facturation")
    @api.depends('create_date')
    def _compute_anne_facturation(self):
        for rec in self:
            if rec.create_date:
                rec.fact_anne_ = rec.create_date.year
            else:
                rec.fact_anne_ = False
    
    partner_id_organisme = fields.Many2one('res.partner', 'Contact')
    move_accord  = fields.Char(string="N° d'accord")
    affiche_partner_id = fields.Integer(string="Afficher Client", default=0)
    
    date_de_prelevement  = fields.Date(compute="_compute_date_prelev",string="Date de prélèvement")    

    @api.depends('invoice_date')
    def _compute_date_prelev(self):
        for rec in self:

            if rec.invoice_date:
                    if rec.invoice_date.day >= 15:
                        date = rec.invoice_date + relativedelta(months=1)
                        rec.date_de_prelevement = date.replace(day=15)
                    else:
                        date = rec.invoice_date
                        rec.date_de_prelevement = date.replace(day=15)

            else:
                rec.date_de_prelevement = False
