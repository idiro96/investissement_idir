# -*- coding: utf-8 -*-

from odoo import models, fields, api

class invistissementMaintenanceLigne(models.Model):
     _name = 'invest.maintenance.ligne'

     date_operation = fields.Date()
     service_fait = fields.Char()
     asset_id = fields.Many2one(comodel_name='account.asset.asset')
     montant = fields.Float()
     piece_comptable = fields.Char()
     personnel_id = fields.Many2one(comodel_name='hr.employee')
     type_operation_id = fields.Many2one(comodel_name='invest.type.operation')
