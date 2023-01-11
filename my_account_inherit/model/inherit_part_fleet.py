from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    helpdesk_fleet_ids = fields.One2many(
        comodel_name="fleet.vehicle",
        inverse_name="partner_id",
        string="Related fleet",
    )


    def action_view_fleet(self):
        return {
            "name": self.name,
            "view_mode": "tree,form",
            "res_model": "fleet.vehicle",
            "type": "ir.actions.act_window",
            "domain": [("partner_id", "child_of", self.id)],
            "context": self.env.context,
        }

    fleet_count = fields.Integer(
        compute="_compute_fleet_count", string="Fleet count"
    )

    #fleet_active_count = fields.Integer(
    #    compute="_compute_fleet_count", string="Fleet active count"
    #)

    #fleet_count_string = fields.Char(
     #   compute="_compute_fleet_count", string="Fleets"
  #  )

    def _compute_fleet_count(self):
        for record in self:
            fleet_ids = self.env["fleet.vehicle"].search(
                [("partner_id", "child_of", record.id)]
            )
            record.fleet_count = len(fleet_ids)

        #    record.fleet_active_count = len(
         #       fleet_ids.filtered(lambda ticket: not ticket.stage_id.closed)
          #  )
          #  count_active = record.fleet_active_count
            #count = record.helpdesk_ticket_count
           # record.fleet_count_string = "{} / {}".format(count_active, count)
