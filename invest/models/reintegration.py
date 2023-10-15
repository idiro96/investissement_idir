# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InvistissementReintegration(models.Model):
    _name = 'invest.reintegration.asset'
    _rec_name = 'motif_reintegration'



    code = fields.Char(String='Code',readonly=True ,default=lambda self: _('New'))
    motif_reintegration = fields.Char()


    @api.model
    def create(self, vals):
        if not vals.get('code') or vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('invest.reintegration.asset') or _('New')

        result = super(InvistissementReintegration, self).create(vals)
        return result
