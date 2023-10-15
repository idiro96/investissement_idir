# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class invistissementAmmortissementMatricielle(models.Model):
     _name = 'invest.ammortissement.matricielle'

     annee = fields.Integer()
     taux = fields.Float()
     categorie_id = fields.Many2one(comodel_name='account.asset.category')