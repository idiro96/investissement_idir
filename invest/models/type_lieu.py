# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class invistissementTypeLieu(models.Model):
    _name = 'invest.type.lieu'
    _inherit = 'mail.thread'
    _rec_name = 'code'

    code = fields.Char()
    intitule = fields.Char()
    parent_id = fields.Many2one(comodel_name='invest.type.lieu')

    @api.multi
    def unlink(self):

        fils = self.env['invest.type.lieu'].search([('parent_id', '=', self.id)])
        if fils:
            raise UserError(
                "Vous ne pouvez pas supprimer cet type de lieu, car ce lieu possède des ascendants")

        endroit = self.env['invest.endroit'].search([('typetest', '=', self.id)])
        if endroit:
            raise UserError(
                "Vous ne pouvez pas supprimer cet type de lieu, car il est utilisée")

        return super(invistissementTypeLieu, self).unlink()
