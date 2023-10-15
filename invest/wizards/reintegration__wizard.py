# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class ReintegrationInvestWizard(models.TransientModel):
    _name = 'reintegration.asset'


    date_reintegration = fields.Date()
    motif_reintegration = fields.Many2one(comodel_name='invest.reintegration.asset')


    @api.multi
    def button_reintegration(self):
        records = self.env['invest.proposer.reforme.asset'].browse(self._context['active_ids'])
        for rec in records:
            asset = self.env['account.asset.asset'].search([('numero_inventaire', '=', rec.num_inventaire)])
            asset.date_reintegration = self.date_reintegration
            asset.motif_reintegration = self.motif_reintegration.motif_reintegration
            if self.date_reintegration < asset.date_propser:
                raise UserError("Date de reintegration doit être supérieur à la date de proposition à la reforme")
            if asset.state == 'reforme':
               asset.state = 'open'
            rec.unlink()
        # for rec in asset:
        #     if rec.state == 'draft':
        #         raise UserError("Vous ne pouver pas proposer à la reforme un mmobilisations non confirmé")
        #
        #     if rec.date_propser:
        #         raise UserError(
        #             "Erreur, vous avez sélectionner des biens qui sont déja proposer a la réforme, veuillez les decocher")
        #
        #     if rec.date_aquisition >= self.date_propser:
        #         raise UserError(
        #             "Erreur, certains bien ont des dates d'acquisition supérieur à la date de proposition a la reforme")

        return {
            'name': 'Reintegration',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.asset.asset',
            'type': 'ir.actions.act_window',
            'domain': [('state', '!=', 'reforme'),('state', '!=', 'close')],
        }