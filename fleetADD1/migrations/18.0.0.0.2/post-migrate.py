def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    Model = env['fleet.vehicle']
    ids = Model.search([]).ids
    for id in ids:
        Model.browse(id)._compute_fleet_user_id()
