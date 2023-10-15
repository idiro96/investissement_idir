# -*- coding: utf-8 -*-

from odoo import models, fields, api
class invistissementDeprciationAnnuel(models.Model):
    _name = 'invest.depreciation.annuel'

    depreciation_date = fields.Date()
    name = fields.Char()
    sequence = fields.Integer()
    amount = fields.Float()
    remaining_value = fields.Float()
    depreciated_value = fields.Float()
    asset_id = fields.Many2one(comodel_name='account.asset.asset')

