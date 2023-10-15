# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class invistissementEndroit(models.Model):
    _name = 'invest.endroit'
    _rec_name = 'intitule'
    _inherit = 'mail.thread'

    code = fields.Char()
    check = fields.Boolean('check')
    intitule = fields.Char()
    parent_id = fields.Many2one(comodel_name='invest.endroit')
    typetest = fields.Many2one(comodel_name='invest.type.lieu')

    # type = fields.Selection([('region', 'Region'), ('site', 'Site'), ('batiment', 'Batiment'), ('bureau', 'Bureau')])
    endroit_ligne_ids = fields.One2many(comodel_name='account.asset.asset', inverse_name='endroit_id_1')

    # def list_affectation(self):
    #     domain = []
    #     team_ids = []
    #     if self.typetest.code == "batiment":
    #         records = self.env['invistissement.endroit'].search([('parent_id', '=', self.id)])
    #         for rec in records:
    #              team_ids = self.env['account.asset.asset'].search([('endroit_id_1', '=', rec.id)])
    #              if team_ids:
    #                 domain.append(('id', 'in', team_ids.ids))
    #              else:
    #                 domain = ''
    #     return {'domain': {'endroit_ligne_ids': domain}}
    # @api.model
    # def create(self, vals):
    #     print('hhhhhhhh')
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Bureau form',
    #         'view_mode': 'form',
    #         'res_model': 'invistissement.endroit',
    #         'view_id': 'endroit_form'
    #     }
    def _get_default_account_ids(self):
        journals = self.env['account.asset.asset'].search([])
        accounts = []
        return accounts

    # @api.onchange('type')
    # def _get_team_id_region_id(self):
    #     """ a function to get a parent_id automatically by selected state"""
    #     for rec in self:
    #         domain = []
    #         rec.parent_id = None
    #         team_ids = []
    #         if self.type == 'endroit':
    #             team_ids = self.env['invistissement.endroit'].search([('type', '=', 'region'),('type', '=', 'site'),('type', '=', 'batiment')])
    #         if self.type == 'site':
    #             team_ids = self.env['invistissement.endroit'].search([('type', '=', 'region')])
    #         elif self.type == 'batiment':
    #             team_ids = self.env['invistissement.endroit'].search([('type', '=', 'site')])
    #         elif self.type == 'bureau':
    #             team_ids = self.env['invistissement.endroit'].search([('type', '=', 'batiment')])
    #
    #         if team_ids:
    #             domain.append(('id', 'in', team_ids.ids))
    #         else:
    #             domain = ''
    #             parent_id = ''
    #     return {'domain': {'parent_id': domain}}

    @api.multi
    def unlink(self):
        import pdb
        pdb.set_trace()
        endroit = self.env['invest.affectation'].search([('endroit_id', '=', self.id)])
        if endroit:
            raise UserError(
                "Vous ne pouvez pas supprimer cet emplacement, car un bien est déja affecté à ce lieu")

        fils = self.env['invest.endroit'].search([('parent_id', '=', self.id)])
        if fils:
            raise UserError(
                "Vous ne pouvez pas supprimer cet emplacement, car ce lieu possède des ascendants")

        return super(invistissementEndroit, self).unlink()
    @api.onchange('typetest')
    def _get_team_id_region_idTest(self):
        """On fait appelle à cette métode pour recupere la liste
        des  parent_id de chaque type d'endroit"""

        for rec in self:
            domain = []
            rec.parent_id = None
            team_ids = []

            for rec2 in self.env['invest.type.lieu'].search([]):
                if self.typetest == rec2:
                    print(self.typetest)
                    print(rec2)
                    parent = self.env['invest.type.lieu'].search([('id', '=', rec2.parent_id.id)]).id
                    print(parent)
                    team_ids = self.env['invest.endroit'].search([('typetest', '=', parent)])
        if team_ids:
            domain.append(('id', 'in', team_ids.ids))
        else:
            domain = ''
            parent_id = ''
        print(domain)
        return {'domain': {'parent_id': domain}}
