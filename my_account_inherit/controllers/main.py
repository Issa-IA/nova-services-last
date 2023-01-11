import base64
import logging

import werkzeug

import odoo.http as http
from odoo.http import request

_logger = logging.getLogger(__name__)


class FleetController(http.Controller):
    @http.route("/fleet/close", type="http", auth="user")
    def support_fleet_close(self, **kw):
        """Close the support fleet"""
        values = {}
        for field_name, field_value in kw.items():
            if field_name.endswith("_id"):
                values[field_name] = int(field_value)
            else:
                values[field_name] = field_value
        fleet = (
            http.request.env["fleet.vehicle"]
            .sudo()
            .search([("id", "=", values["fleet_id"])])
        )
        fleet.state_id = values.get("state_id")

        return werkzeug.utils.redirect("/my/fleets/" + str(fleet.id))

    @http.route("/new/ticket", type="http", auth="user", website=True)
    def create_new_ticket(self, **kw):
        categories = http.request.env["fleet.vehicle"].search(
            [("active", "=", True)]
        )
        email = http.request.env.user.email
        name = http.request.env.user.name
        return http.request.render(
            "my_account_inherit.portal_create_fleet",
            {"name": name},
        )

    @http.route("/submitted/fleet", type="http", auth="user", website=True, csrf=True)
    def submit_fleet(self, **kw):
        vals = {
            "company_id": http.request.env.user.company_id.id,

            "name": kw.get("subject"),
            "attachment_ids": False,

            "partner_id": request.env.user.partner_id.id,
            "partner_name": request.env.user.partner_id.name,
            "partner_email": request.env.user.partner_id.email,
        }
        new_fleet = request.env["fleet.vehicle"].sudo().create(vals)
        new_fleet.message_subscribe(partner_ids=request.env.user.partner_id.ids)
        if kw.get("attachment"):
            for c_file in request.httprequest.files.getlist("attachment"):
                data = c_file.read()
                if c_file.filename:
                    request.env["ir.attachment"].sudo().create(
                        {
                            "name": c_file.filename,
                            "datas": base64.b64encode(data),
                            "res_model": "fleet.vehicle",
                            "res_id": new_fleet.id,
                        }
                    )
        return werkzeug.utils.redirect("/my/fleets")

