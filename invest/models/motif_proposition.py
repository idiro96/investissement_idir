# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class invistissementMotifPropostion(models.Model):
    _name = 'invest.motif.propostion.asset'
    _rec_name = 'motif_propostion1'



    code = fields.Char(String='Code',readonly=True ,default=lambda self: _('New'))
    motif_propostion1 = fields.Char()


    @api.model
    def create(self, vals):
        if not vals.get('code') or vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('invest.motif.propostion.asset') or _('New')

        result = super(invistissementMotifPropostion, self).create(vals)
        return result
