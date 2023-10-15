# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class invistissementProvenanceBien(models.Model):
    _name = 'invest.provenance.bien.asset'
    _rec_name = 'provenance_bien'



    code = fields.Char(String='Code',readonly=True ,default=lambda self: _('New'))
    provenance_bien = fields.Char()


    @api.model
    def create(self, vals):
        if not vals.get('code') or vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('invest.provenance.bien.asset') or _('New')

        result = super(invistissementProvenanceBien, self).create(vals)
        return result
