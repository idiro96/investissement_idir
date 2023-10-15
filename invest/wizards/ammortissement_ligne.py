# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

from odoo.exceptions import UserError


class invistissementAmmortissementLigne(models.TransientModel):
    _name = 'ammortissement.ligne'
    _rec = 'annee'

    type = fields.Selection([('linear', 'Linéaire'), ('degressive', 'Dégressif')])
    nbr_annee = fields.Integer()
    annee = fields.Integer()
    taux = fields.Float()
    categorie_id = fields.Many2one(comodel_name='account.asset.category')
    ammortissement_ligne_ids = fields.One2many(comodel_name='ammortissement.ligne', inverse_name='id')
    domain = []
    def essai(self):

        for rec in self:
            rec.parent_id = None
            team_ids = []
            team_ids = self.env['ammortissement.ligne'].search([])
            print("Rabah2")
            print(team_ids)
        if team_ids:
           self.domain.append(('id', 'in', team_ids.ids))
        else:
            domain = ''
            parent_id = ''
        print(self.domain)

        print(self.annee)
        print(self.ammortissement_ligne_ids)
        return {'domain': {'ammortissement_ligne_ids': self.domain},
                'type': 'ir.actions.do_nothing',
                }

    def enregistrer(self):

        record = self.env['account.asset.category'].browse(self._context['active_id'])
        record.write({'method_number': self.nbr_annee})
        record.write({'method': self.type})
        change_type_control(self, record)
        i = 0
        for rec1 in self.env['ammortissement.ligne'].search([]):
            i = i + 1
            if i > self.nbr_annee + 1:
                raise UserError("Nombre de ligne dépasse ou inférieur au  nombre d'année d'ammortissement")
            if rec1.annee >  self.nbr_annee +1 :
                raise UserError("Vérifier que l'année saisie n 'est pas supérieure au nombre d'année d'ammortissemen ")

        for rec in self.env['ammortissement.ligne'].search([]):

                ammortissement = self.env['invest.ammortissement.matricielle'].create({
                    'annee': rec.annee,
                    'taux': rec.taux / 100,
                    'categorie_id': record.id
                })
                print("eae")
                record.write({'method_progress_factor': rec.taux / 100})
                print(rec.taux / 100)

        for record1 in self.env['invest.ammortissement.matricielle'].search([('taux', '=', 0)]):
                record1.unlink()


def change_type_control(self,record):
    assets = self.env['account.asset.asset'].search([('category_id', '=', record.id)])
    if self.type == 'linear':
        for record1 in self.env['invest.ammortissement.matricielle'].search([('categorie_id', '=', record.id)]):
            if assets:
                raise UserError(
                    "Vous ne pouvez pas effectue une modification car cette catégorie est reliée déja à des immobilisations")
            else:
                record1.unlink()
    else:
        if assets:
            raise UserError(
                "Vous ne pouvez pas effectue une modification car cette catégorie est reliée déja à des immobilisations")
        else:
            for record1 in self.env['invest.ammortissement.matricielle'].search(
                    [('categorie_id', '=', record.id)]):
                if assets:
                    raise UserError(
                        "Vous ne pouvez pas effectue une modification car cette catégorie est reliée déja à des immobilisations")
                else:
                    record1.unlink()

