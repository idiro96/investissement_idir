# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class invistissementAffectation(models.Model):
     _name = 'invest.affectation'

     annee = fields.Integer()
     observation = fields.Char()
     fin_affectation = fields.Date('Fin affectation')
     employee_id = fields.Many2one(comodel_name='hr.employee')
     structure_id = fields.Many2one(comodel_name='hr.department')
     asset_id = fields.Many2one(comodel_name='account.asset.asset')
     endroit_id = fields.Many2one(comodel_name='invest.endroit')
     date_affectation = fields.Date('Date affectation')


