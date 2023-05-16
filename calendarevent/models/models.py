from odoo import models, fields, api


class   Calendarinherit(models.Model):
    _inherit = "calendar.event"
    def write(self, vals):
        #mail_notrack = True
        #self = self.with_context(trackin_disabel=True)
        res = super(Calendarinherit, self.with_context(mail_notrack=True)).write(vals)
        return res
    
    def create(self, vals):
        #mail_notrack = True
        #super(Task, self.with_context(mail_notrack=True)).create(vals)
        #self = self.with_context(trackin_disabel=True)
        res = super(Calendarinherit, self.with_context(mail_notrack=True)).create(vals)
        return res
    
    #def action_open_composer(self): 
    #    partner_ids = self.partner_ids
    #    if len(self.partner_ids) > 1:
    #                x_id = self.partner_ids[1].id
    #                self.partner_ids = [(3, x_id)]
    #    result = super(Calendarinherit, self).action_open_composer()   
    #    self.partner_ids = partner_ids
    #    return result

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


