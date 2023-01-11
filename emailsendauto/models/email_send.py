from odoo import _, api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
class sale_order(models.Model):
    _inherit = 'sale.order'
    sale_year_email = fields.Integer("nombre exact de mail par an ", default=0)
    sale_month_email = fields.Integer("nombre exact de mail 6 mois ", default=0)
    def send_contrat_email(self):
        six_months = date.today() + relativedelta(months=+6)
        tow_years = date.today() + relativedelta(years=+2)
        #six_months = date.today() + relativedelta(days=+1)
        #tow_years = date.today() + relativedelta(days=+2)
        sale_parc = self.env['sale.order'].search([('sale_park', '=', True)])
        six_months_sale = []
        tow_years_sale = []
        if sale_parc:
            for rec in sale_parc:
                fleet_six = self.env['fleet.vehicle'].search([('fleet_devis_id', '=', rec.id), ('fleet_expiration_date', 'like', six_months)])
                fleet_year = self.env['fleet.vehicle'].search([('fleet_devis_id', '=', rec.id), ('fleet_expiration_date', 'like', tow_years)])
                if fleet_six:
                    six_months_sale.append(rec)
                    if rec.partner_id.type_contact=="Prospect":
                        rec.sale_month_email = 1
                    print("id", rec.id)
                    print("sale_month_email",rec.sale_month_email)
                if fleet_year:
                    tow_years_sale.append(rec)
                    if rec.partner_id.type_contact == "Client":
                        rec.sale_year_email = 1
                    print("id", rec.id)
                    print("sale_year_email", rec.sale_year_email)




