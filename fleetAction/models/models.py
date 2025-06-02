from odoo import models, fields, api
from datetime import date, datetime

import math
from dateutil.relativedelta import relativedelta

class FleetVehicleHerit(models.Model):
    _inherit = 'fleet.vehicle'
    ########################## update date ####
    def updateDate(self):
        fleet_parc_all= self.env['fleet.vehicle'].search([])

        for rec in fleet_parc_all:
            if rec.fleet_expiration_date:
                if rec.fleet_expiration_date > date.today():
                    if rec.fleet_periodicite == 'mens':
                        date1 = date.today() - relativedelta(days=1)
                        date2 = rec.fleet_expiration_date
                        num_months = (date2.year - date1.year) * 12 + (date2.month - date1.month)
                        if num_months > 1:
                            rec.fleet_duree_rest = num_months - 1
                        else:
                            rec.fleet_duree_rest = 0
                    elif rec.fleet_periodicite == 'trim':
                        date1 = date.today() - relativedelta(days=1)
                        date2 = rec.fleet_expiration_date
                        num_months = (date2.year - date1.year) * 12 + (date2.month - date1.month)
                        rec.fleet_duree_rest = math.floor(num_months / 3)
                    else:
                        rec.fleet_duree_rest = 0
                else:
                    rec.fleet_duree_rest = 0
            else:
                rec.fleet_duree_rest = 0

            rec.fleet_solde_est = rec.fleet_prix_HT * rec.fleet_duree_rest








