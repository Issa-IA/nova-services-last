def createParck(self):
    print("bbbbbbbbbbbbbbb")

    return {
        'type': 'ir.actions.act_window',
        'name': " ",
        'res_model': 'creatpark',
        'view_mode': 'form',
        'target': 'new',
        'context': {'default_devis_dossier': self.id},
    }


def action_confirm(self):
    res = super(SaleOrderHerit, self).action_confirm()
    if self.partner_id:
        self.partner_id.type_contact = "Client"
    return self.createParck()


############## fin pop up


#################### récupurer le numéro de dossier dans parc matériels
"""
@api.onchange("sale_parc_id","name")
def fleetDevisID(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_dossier_devis = rec.name



##################
##########                infos CONTRATS Automatique
##################
@api.onchange("sale_parc_id", "sale_type")
def fleetType(self):
    for rec in self:
        if rec.sale_parc_id:
            if rec.sale_type == 'location':
                rec.sale_parc_id.fleet_type = 'location'
            if rec.sale_type == 'vente':
                rec.sale_parc_id.fleet_type = 'vente'

@api.onchange("sale_periodicite", "sale_parc_id")
def fleetPeriodicite(self):
    for rec in self:
        if rec.sale_parc_id:
            if rec.sale_periodicite == 'trim':
                rec.sale_parc_id.fleet_periodicite = 'trim'
                rec.sale_parc_id.fleet_facturation = 'trim'
            if rec.sale_periodicite == 'mens':
                rec.sale_parc_id.fleet_periodicite = 'mens'
                rec.sale_parc_id.fleet_facturation = 'mens'

@api.onchange("sale_parc_id", "sale_loyer")
def fleetPrixHT(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_prix_HT = rec.sale_loyer

@api.onchange("sale_parc_id", "sale_duree")
def fleetDuree(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_duree = rec.sale_duree

@api.onchange("sale_parc_id", "sale_leaser")
def fleetLeaser(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_leaser = rec.sale_leaser

@api.onchange("sale_parc_id", "sale_accord")
def fleetAccord(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_accord = rec.sale_accord
##################
##########                infos MAINTENANCE Automatique
##################
@api.onchange("sale_parc_id", "sale_cout_signe_col")
def fleetCoutCouleur(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_cout_Couleur = rec.sale_cout_signe_col

@api.onchange("sale_parc_id", "sale_forfait_signe_col")
def fleetorForfaitCouleur(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_forfait_couleur = rec.sale_forfait_signe_col

@api.onchange("sale_parc_id", "sale_cout_signe_nb")
def fleetorCoutNb(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_cout_nb = rec.sale_cout_signe_nb

@api.onchange("sale_parc_id", "sale_forfait_signe_nb")
def fleetorForfaitNB(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_forfait_nb = rec.sale_forfait_signe_nb

@api.onchange("sale_parc_id", "sale_abonnement_service")
def fleetorAbonnementService(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_abonnement_service = rec.sale_abonnement_service

@api.onchange("sale_parc_id", "sale_autre_frais")
def fleetorAutre(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_autre = rec.sale_autre_frais
##################
##########                infos FINANCIERES Automatique
##################

@api.onchange("sale_parc_id", "sale_partenariat")
def fleetPartenariat(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_partenariat = rec.sale_partenariat

@api.onchange("sale_parc_id", "sale_solde_2_fois")
def fleetSoldefois(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_solde_fois = rec.sale_solde_2_fois

@api.onchange("sale_parc_id", "sale_date_fin_F")
def fleetDateFin(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_date_fin_F = rec.sale_date_fin_F

@api.onchange("sale_parc_id", "sale_date_2_solde")
def fleetDateSoldefois(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_date_2_solde = rec.sale_date_2_solde

@api.onchange("sale_parc_id","sale_periodicite","sale_duree")
def fleetDateEXpiration(self):
    for rec in self:
        if rec.sale_parc_id:
                if rec.sale_periodicite == 'mens':
                    if rec.sale_duree > 0:
                        rec.sale_parc_id.fleet_expiration_date = date.today() + relativedelta(
                            months=rec.sale_duree) - relativedelta(days=1)
                    else:
                        rec.sale_parc_id.fleet_expiration_date = date.today()

                if rec.sale_periodicite == 'trim':
                    if rec.sale_duree > 0:
                        rec.sale_parc_id.fleet_expiration_date = date.today() + relativedelta(
                            months=(rec.sale_duree * 3)) - relativedelta(days=1)
                    else:
                        rec.sale_parc_id.fleet_expiration_date = date.today()

@api.onchange("sale_parc_id")
def fleetDateInstalation(self):
    for rec in self:
        if rec.sale_parc_id:
            rec.sale_parc_id.fleet_date_inst =date.today()
"""

########## fin auto
