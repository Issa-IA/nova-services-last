from odoo import models, fields, api


class   Calendarinherit(models.Model):
    _inherit = "calendar.event"

    @api.onchange("partner_ids")
    def update_location(self):
        for rec in self:
            if rec.partner_ids:
                if rec.partner_ids[0].zip and rec.partner_ids[0].city and rec.partner_ids[0].street:
                    rec.location =str(rec.partner_ids[0].street)+' '+ str(rec.partner_ids[0].zip) + ' ' + str(rec.partner_ids[0].city)
                if rec.partner_ids[0].zip and not rec.partner_ids[0].city and not rec.partner_ids[0].street:
                    rec.location = str(rec.partner_ids[0].zip)
                if not rec.partner_ids[0].zip and rec.partner_ids[0].city and not rec.partner_ids[0].street:
                    rec.location = str(rec.partner_ids[0].city)
                if not rec.partner_ids[0].zip and not rec.partner_ids[0].city and  rec.partner_ids[0].street:
                    rec.location = str(rec.partner_ids[0].street)
                if not rec.partner_ids[0].zip and  rec.partner_ids[0].city and  rec.partner_ids[0].street:
                    rec.location = str(rec.partner_ids[0].street) +' '+ str(rec.partner_ids[0].city)
                if  rec.partner_ids[0].zip and  not rec.partner_ids[0].city and  rec.partner_ids[0].street:
                    rec.location = str(rec.partner_ids[0].street) +' '+ str(rec.partner_ids[0].zip)


