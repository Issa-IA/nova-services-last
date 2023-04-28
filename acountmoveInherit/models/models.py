from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class MoveLineHerit(models.Model):
    _inherit = "account.move.line"
    ############ if one serie number
    move_line_serie = fields.Char(string="N° serie")
    ############


class AcountMoveHerit(models.Model):
    _inherit = 'account.move'
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
