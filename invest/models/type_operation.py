# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class invistissementTypeOperation(models.Model):
    _name = 'invest.type.operation'
    _rec_name = 'intitule'

    code = fields.Char()
    intitule = fields.Char()
    maintenance_ligne_ids = fields.One2many(comodel_name='invest.maintenance.ligne', inverse_name='type_operation_id')


    @api.model
    def create(self, vals):
        if not vals.get('code') or vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('invest.type.operation') or _('New')

        result = super(invistissementTypeOperation, self).create(vals)
        return result