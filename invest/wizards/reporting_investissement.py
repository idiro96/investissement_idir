# -*- coding: utf-8 -*-

from odoo import models, fields, api


class invistissementReportingAsset(models.TransientModel):
    _name = 'reporting.investissement'

    category_id = fields.Many2one(comodel_name='account.asset.category')
    report_typ = fields.Selection(
        [('detaille', 'Tableau des amortissements detaille'),('repertoire', 'Repertoire des investissements'),('repertoire_fv', 'Repertoire des investissements faible valeur'),('sortie', 'repertoire des investissements sortie'),('sortie_fb', 'repertoire des investissements sortie faible valeur'),('reforme', 'repertoire des investissements proposer à la reforme')],
        required=True, default='accounts')
    structure_id = fields.Many2one(comodel_name='hr.department')
    date_au = fields.Date(string="Au", required=True)
    date_du = fields.Date(string="Du")
    asset_ids = fields.One2many(comodel_name='account.asset.asset', inverse_name='id')
    etat_asset_id = fields.Many2one(comodel_name='invest.etat.asset')
    motif_propostion = fields.Many2one(comodel_name='invest.motif.propostion.asset')
    mise_attente = fields.Many2one(comodel_name='invest.mise.attente.asset')

    def print_investissement_report(self):
        data = {
            'model': 'reporting.investissement',
            'form': self.read()[0],
        }
        if self.report_typ == 'detaille':
            return self.env.ref("invest.action_tableau_des_amortissements_detaille_report").report_action(self, data=data)
        elif self.report_typ == 'repertoire':
            return self.env.ref("invest.action_repertoire_investissements_report").report_action(self, data=data)
        elif self.report_typ == 'sortie':
            return self.env.ref("invest.action_repertoire_invest_etat").report_action(self,data=data)
        elif self.report_typ == 'sortie_fb':
            return self.env.ref("invest.action_repertoire_invest_etat_fb").report_action(self,data=data)
        elif self.report_typ == 'reforme':
            return self.env.ref("invest.action_repertoire_invest_reforme").report_action(self, data=data)
        else:
            return self.env.ref("invest.action_repertoire_des_investissements_faible_valeur").report_action(self, data=data)

