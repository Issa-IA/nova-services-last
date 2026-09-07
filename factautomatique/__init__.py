# -*- coding: utf-8 -*-

from . import controllers
from . import models


def _backfill_fact_date_derniere_facturation(cr, registry):
    """Initialise le champ fact_date_derniere_facturation pour les matériels déjà
    facturés par le passé (à partir du dernier bon de commande de facturation
    automatique enregistré dans listboncommandefleet).

    Sans ce backfill, la protection anti-doublon ajoutée dans create_facturation
    (voir fleet.vehicle._periode_deja_facturee) ne s'appliquerait qu'à partir du
    prochain cycle de facturation de chaque dossier, et ne protégerait pas contre un
    doublon qui se reproduirait juste après la mise à jour du module.
    """
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    Fleet = env['fleet.vehicle']
    Bon = env['listboncommandefleet']

    fleets = Fleet.search([('fact_date_derniere_facturation', '=', False)])
    for fleet in fleets:
        dernier_bon = Bon.search([('fleet_id', '=', fleet.id)], order='id desc', limit=1)
        if dernier_bon and dernier_bon.devis_id and dernier_bon.devis_id.date_order:
            fleet.fact_date_derniere_facturation = dernier_bon.devis_id.date_order.date()
