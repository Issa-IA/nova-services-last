# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class CustomerPortalFleet(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        fleet_count = request.env["fleet.vehicle"].search_count(
            [("partner_id", "child_of", partner.id)]
        )
        values["fleet_count"] = fleet_count
        return values

    @http.route(
        ["/my/fleets", "/my/fleets/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_fleets(
        self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        PortalFleet = request.env["fleet.vehicle"].search([("partner_id", "child_of", partner.id)])
        domain = [("partner_id", "child_of", partner.id)]

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
            "state": {"label": _("State"), "order": "state_id"},

        }
        searchbar_filters = {"all": {"label": _("All"), "domain": []}}
        for state in request.env["fleet.vehicle.state"].search([]):
            searchbar_filters.update(
                {
                    str(state.id): {
                        "label": state.name,
                    "domain": [("state_id", "=", state.id)],
                    }
                }
            )

        #default sort by order
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        # default filter by value
        if not filterby:
            filterby = "all"
        domain += searchbar_filters[filterby]["domain"]

        # count for pager
        fleet_count = PortalFleet.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/fleets",
            url_args={},
            total=fleet_count,
            page=page,
            step=self._items_per_page,
        )
        # content according to pager and archive selected
        fleets = PortalFleet.search(
            domain, limit=self._items_per_page, offset=pager["offset"]
        )
        values.update(
            {
                "date": date_begin,
                "fleets": fleets,
                "page_name": "fleets",
                "pager": pager,
                "default_url": "/my/fleets",
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
                "searchbar_filters": searchbar_filters,
                "filterby": filterby,
            }
        )
        return request.render("my_account_inherit.portal_my_fleets", values)

    @http.route(
        ["/my/fleet/<int:fleet_id>"], type="http", auth="public", website=True
    )
    def portal_my_fleet(self, fleet_id=None, access_token=None, **kw):
        try:
            fleet_sudo = self._document_check_access(
                "fleet.vehicle", fleet_id, access_token=access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        values = self._fleet_get_page_view_values(fleet_sudo, **kw)
        return request.render("my_account_inherit.portal_fleet_page", values)

    def _fleet_get_page_view_values(self, fleet, **kwargs):
        closed_stages = request.env["fleet.vehicle.state"]
        values = {
            "page_name": "Parc Matériel",
            "fleet": fleet,
        }
        return values

