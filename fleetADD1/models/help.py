if self.devis_dossier.order_line:
    if self.devis_dossier.sale_periodicite == 'mens':
        if self.devis_dossier.sale_duree:
            if self.devis_dossier.sale_duree > 0:
                expiration_date = date.today() + relativedelta(
                    months=self.devis_dossier.sale_duree) - relativedelta(days=1)
            else:
                expiration_date = date.today()
        else:
            expiration_date = False


    elif self.devis_dossier.sale_periodicite == 'trim':
        if self.devis_dossier.sale_duree:
            if self.devis_dossier.sale_duree > 0:
                expiration_date = date.today() + relativedelta(
                    months=(self.devis_dossier.sale_duree * 3)) - relativedelta(days=1)
            else:
                expiration_date = date.today()
        else:
            expiration_date = False

    else:
        expiration_date = False

    for rec in self.devis_dossier.order_line:
        if rec.product_id.parc_ok:
            if self.devis_dossier.sale_leaser:
                sale_leaser = self.devis_dossier.sale_leaser.id
            else:
                sale_leaser = False

            vals = {'fleet_serie': rec.product_id.name,
                    'fleet_artic_id': rec.product_id.id,
                    'fleet_expiration_date': expiration_date,
                    'fleet_type': self.devis_dossier.sale_type,
                    'fleet_periodicite': self.devis_dossier.sale_periodicite,
                    'fleet_facturation': self.devis_dossier.sale_periodicite,
                    'fleet_prix_HT': self.devis_dossier.sale_loyer,
                    'fleet_duree': self.devis_dossier.sale_duree,
                    'fleet_leaser': sale_leaser,
                    'fleet_accord': self.devis_dossier.sale_accord,
                    'fleet_cout_Couleur': self.devis_dossier.sale_cout_signe_col,
                    'fleet_forfait_couleur': self.devis_dossier.sale_forfait_signe_col,
                    'fleet_cout_nb': self.devis_dossier.sale_cout_signe_nb,
                    'fleet_forfait_nb': self.devis_dossier.sale_forfait_signe_nb,
                    'fleet_abonnement_service': self.devis_dossier.sale_abonnement_service,
                    'fleet_autre': self.devis_dossier.sale_autre_frais,
                    'fleet_partenariat': self.devis_dossier.sale_partenariat,
                    'fleet_solde_fois': self.devis_dossier.sale_solde_2_fois,
                    'fleet_date_fin_F': self.devis_dossier.sale_date_fin_F,
                    'fleet_date_2_solde': self.devis_dossier.sale_date_2_solde,
                    'fleet_date_inst': date.today(),
                    'fleet_dossier_devis': self.devis_dossier.name,
                    'fleet_devis_id': self.devis_dossier.id,
                    }
            self.env['fleet.vehicle'].create(vals)