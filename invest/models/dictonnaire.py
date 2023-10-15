# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InvistissementDictonnaire(models.Model):
    _name = 'invest.dictonnaire'
    _rec_name = 'designation'

    code = fields.Char(String='Code',readonly=True ,default=lambda self: _('New'))
    designation = fields.Char()
    category_id1 = fields.Many2one(comodel_name='account.asset.category')

    @api.model
    def create(self, vals):
        if not vals.get('code') or vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('invest.dictonnaire') or _('New')

        result = super(InvistissementDictonnaire, self).create(vals)
        return result