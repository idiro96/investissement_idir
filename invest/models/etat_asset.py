# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class invistissementEtatAsset(models.Model):
    _name = 'invest.etat.asset'
    _rec_name = 'designation'


    code = fields.Char(String='Code',readonly=True ,default=lambda self: _('New'))
    designation = fields.Char(String='Désignation')


    @api.model
    def create(self, vals):
        if not vals.get('code') or vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('invest.etat.asset') or _('New')

        result = super(invistissementEtatAsset, self).create(vals)
        return result
