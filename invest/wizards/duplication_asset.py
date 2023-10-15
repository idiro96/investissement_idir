# -*- coding: utf-8 -*-
from datetime import time

from odoo import models, fields, api
from odoo.addons.account_asset.models.account_asset import AccountAssetAsset


class invistissementDuplicationAsset(models.TransientModel):
    _name = 'duplication.asset'

    duplication = fields.Integer()

    def button_duplication(self):
        asset = self.env['account.asset.asset'].browse(self._context['active_id'])
        t = 0
        while t < self.duplication:
            t = t + 1
            asset_ligne = asset.env['account.asset.asset'].create({
            'name': asset.name,
            'code': asset.code,
            'value': asset.value,
            'category_id': asset.category_id.id,
            'date': asset.date,
            # 'state': asset.state,
            'active': asset.active,
            'method': asset.method,
            'method_number': asset.method_number,
            'method_period': asset.method_period,
            'method_end': asset.method_end,
            'method_progress_factor': asset.method_progress_factor,
            'prorata': asset.prorata,
            'message_last_post': asset.message_last_post,
            'salvage_value': asset.salvage_value,
            # 'numero_inventaire': asset.numero_inventaire,
            # 'barcode_image': asset.barcode_image,
            'tva': asset.tva,
            'ttc': asset.ttc,
            'date_aquisition': asset.date_aquisition,
            'type_entrer': asset.type_entrer,
            'invoice_id': asset.invoice_id.id,
            'demande_achat': asset.demande_achat,
            'date_demande_achat': asset.date_demande_achat,
            'num_bon_commande': asset.num_bon_commande,
            'structure_id_achat': asset.structure_id_achat.id,
            'demandeur_achat': asset.demandeur_achat.id,
            'piece_entrer': asset.piece_entrer,
            'date_piece_entrer': asset.date_piece_entrer,
            'date_transfert': asset.date_transfert,
            'provenance_bien': asset.provenance_bien.id,
            'vnc': asset.vnc,
            'partner_id': asset.partner_id.id,

        })

