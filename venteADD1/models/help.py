"""
< group >
< group >
< group >
< field
name = "sale_cout_signe_nb" / >
< field
name = "sale_cout_actuel_nb" / >
< field
name = "sale_cout_actuel_signe_nb" / >
< / group >
< group >

< field
name = "sale_cout_signe_col" / >
< field
name = "sale_cout_actuel_col" / >
< field
name = "sale_cout_actuel_signe_col" / >
< / group >
< / group >
< group >
< group >
< field
name = "sale_forfait_signe_nb" / >
< field
name = "sale_forfait_actuel_nb" / >
< field
name = "sale_forfait_actuel_signe_nb" / >
< / group >
< group >
< field
name = "sale_forfait_signe_col" / >
< field
name = "sale_forfait_actuel_col" / >
< field
name = "sale_forfait_actuel_signe_col" / >
< / group >
< / group >
< group >
< group >
< field
name = "sale_abonnement_service" / >
< field
name = "sale_autre_frais" / >
< / group >
< / group >

< / group >

"""

vals = {         'partner_id': self.id,
                    'annee': "2022",
                    }
self.env['budget.partenariat'].create(vals)
vals = {         'partner_id': self.id,
                    'annee': "2023",
                    }
self.env['budget.partenariat'].create(vals)
vals = {         'partner_id': self.id,
                    'annee': "2024",
                    }
self.env['budget.partenariat'].create(vals)
self.env['budget.partenariat'].create(vals)
vals = {         'partner_id': self.id,
                    'annee': "2025",
                    }
self.env['budget.partenariat'].create(vals)
vals = {         'partner_id': self.id,
                    'annee': "2026",
                    }
self.env['budget.partenariat'].create(vals)