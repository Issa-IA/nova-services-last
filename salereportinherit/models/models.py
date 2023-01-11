from odoo import models, fields, api

class SaleReportHerit(models.Model):
    _inherit = 'sale.report'
    sale_marge_report  = fields.Float(string="%MC tot", readonly=True)
    sale_chifre_report = fields.Float(string="%CA tot", readonly=True)
    sale_client_report = fields.Float(string="%NB Client tot", readonly=True)
    sale_contrat_report = fields.Float(string="%NB Contrat tot", readonly=True)


    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['sale_marge_report'] = ", SUM(s.sale_comer) AS sale_marge_report"
        fields['sale_chifre_report'] = ", SUM(s.sale_chifre_aff) AS sale_chifre_report"    
        fields['sale_contrat_report'] = ", SUM(s.sale_contrat_tot) AS sale_contrat_report"
        fields['sale_client_report'] = ", SUM(s.sale_client_tot) AS sale_client_report" 
        return super(SaleReportHerit, self)._query(with_clause, fields, groupby, from_clause)



