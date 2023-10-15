# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class invistissementSousCompte(models.Model):
    _name = 'invest.sous.compte.asset'
    _rec_name = 'compte'



    compte = fields.Many2one(comodel_name='account.account')
    code = fields.Char(String='Code')
    libelle = fields.Char(String='Libellé')



