# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class SortieInvestWizard(models.TransientModel):
    _name = 'sortie.asset'

    etat_asset_id = fields.Many2one(comodel_name='invest.etat.asset')
    date_sorti = fields.Date()


    def button_sortie(self):
        records = self.env['invest.proposer.reforme.asset'].browse(self._context['active_ids'])
        for rec in records:
            if self.date_sorti < rec.date_propser:
                raise UserError("Date de sortie doit être supérieur à la date de proposition à la reforme")
            asset = self.env['account.asset.asset'].search([('numero_inventaire', '=', rec.num_inventaire)])
            asset.date_sorti = self.date_sorti
            asset.etat_asset_id = self.etat_asset_id
            if asset.state == 'reforme':
               asset.state = 'close'
            rec.unlink()
            depreciations = self.env['account.asset.depreciation.line'].search([('asset_id.id', '=', asset.id),('depreciation_date', '>', asset.date_sorti)])
            for rec1 in depreciations:
                print('test 123456')
                rec1.unlink()

        return {
            'name': 'SortieInvest',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.asset.asset',
            'type': 'ir.actions.act_window',
            'domain': [('state', '=', 'close')],
        }
        # for rec in records:
        #     if rec.date_sorti:
        #         raise UserError(
        #             "Erreur, vous avez sélectionner des biens qui sont déja sorties, veuillez les decocher")
        #
        #     if rec.date_aquisition >= self.date_sorti:
        #         raise UserError(
        #             "Erreur, certains bien ont des dates d'acquisition supérieur à la date de sortie")

            # if self.date_sorti >= rec.date_propser:
            #     raise UserError(
            #         "Erreur, certains bien ont des dates de propostion a la reforme  supérieur à la date de sortie")

        # for rec in records:
        #     if not rec.date_sorti:
        #         rec.etat_asset_id = self.etat_asset_id
        #         rec.date_sorti = self.date_sorti
        #         rec.state = "close"