# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class invistissementMiseAttente(models.Model):
    _name = 'invest.mise.attente.asset'
    _rec_name = 'mise_attente1'



    code = fields.Char(String='Code',readonly=True ,default=lambda self: _('New'))
    mise_attente1 = fields.Char()


    @api.model
    def create(self, vals):
        if not vals.get('code') or vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('invest.mise.attente.asset') or _('New')

        result = super(invistissementMiseAttente, self).create(vals)
        return result
