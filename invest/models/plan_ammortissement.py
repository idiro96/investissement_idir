# -*- coding: utf-8 -*-

from odoo import models, fields, api

class invistissementplanAmmortissement(models.Model):
     _name = 'invest.plan.ammortissement'

     annee = fields.Integer()
     valeur_origine = fields.Float()
     intuitee = fields.Float()
     cummule = fields.Float()
     vnc = fields.Float()