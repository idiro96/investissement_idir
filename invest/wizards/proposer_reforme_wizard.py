# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class ProposerReformeWizard(models.TransientModel):
    _name = 'proposer.reforme.asset'


    date_propser = fields.Date()
    motif_propostion = fields.Many2one(comodel_name='invest.motif.propostion.asset')
    mise_attente = fields.Many2one(comodel_name='invest.endroit')

    def button_proposer_reforme(self):
        record1 = self.env['account.asset.asset'].browse(self._context['active_ids'])
        for rec in record1:
            if not rec.date_propser:
                proposer_reforme(self,rec)
            else:
                re_proposer_reforme(self,rec)

@api.multi
def proposer_reforme(self,asset):
        if asset.state == 'draft':
            raise UserError("Vous ne pouvez pas proposer à la reforme un mmobilisations non confirmé")

        if asset.date_propser:
            raise UserError("Erreur, vous avez sélectionné des biens qui sont déja proposer a la réforme, veuillez les decocher")

        if asset.date_aquisition >= self.date_propser:
            raise UserError("Erreur, certains bien ont des dates d'acquisition supérieur à la date de proposition a la reforme")

        if not asset.date_propser:
            asset.date_propser = self.date_propser
            asset.motif_propostion2 = self.motif_propostion.motif_propostion1
            asset.mise_attente2 = self.mise_attente.id

        asset_ligne1 = asset.env['invest.proposer.reforme.asset'].create({
            'date_propser': self.date_propser,
            'motif_propostion1': self.motif_propostion.id,
            'mise_attente1': self.mise_attente.id,
            'value': asset.value,
            'name': asset.name,
            'num_inventaire': asset.numero_inventaire,
            'date_aqui': asset.date_aquisition,
        })
        if asset.state == 'open':
           asset.state = 'reforme'
           # rec.unlink()
        return {
            'name': 'Proposer Reforme',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'invest.proposer.reforme.asset',
            'type': 'ir.actions.act_window',
            # 'domain': [('state', '=', 'reforme')],

        }
@api.multi
def re_proposer_reforme(self,asset):
        if asset.state == 'close':
            raise UserError("Vous ne pouvez pas affecter un bien réformer")

        if asset.date_propser > self.date_propser:
            raise UserError("la nouvelle date de propostion doit étre supérieur à l'anciene")
        else:
            asset.date_propser = self.date_propser

        asset_ligne1 = asset.env['invest.proposer.reforme.asset'].create({
            'date_propser': self.date_propser,
            'motif_propostion1': self.motif_propostion.id,
            'mise_attente1': self.mise_attente.id,
            'value': asset.value,
            'name': asset.name,
            'num_inventaire': asset.numero_inventaire,
            'date_aqui': asset.date_aquisition,
        })
        if asset.state == 'open':
           asset.state = 'reforme'
           # rec.unlink()
        return {
            'name': 'Proposer Reforme',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'invest.proposer.reforme.asset',
            'type': 'ir.actions.act_window',
            # 'domain': [('state', '=', 'reforme')],

        }