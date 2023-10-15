# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class invistissementProposerReforme(models.Model):
    _name = 'invest.proposer.reforme.asset'



    date_propser = fields.Date()
    motif_propostion1 = fields.Many2one(comodel_name='invest.motif.propostion.asset')
    mise_attente1 = fields.Many2one(comodel_name='invest.endroit')
    num_inventaire = fields.Char()
    name = fields.Char()
    date_aqui = fields.Date()
    value = fields.Float()





