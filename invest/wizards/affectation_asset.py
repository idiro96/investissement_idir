# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api, _
from odoo.addons.account_asset.models.account_asset import AccountAssetAsset
from odoo.exceptions import UserError

from my_addons.invest.models.account_asset_asset_inherit import générer_code_barre


class invistissementAffectationAsset(models.TransientModel):
    _name = 'affectation.asset'
    _description = 'Affectation Wizard'


    date_affectation = fields.Date()
    annee = fields.Integer()
    observation = fields.Char()
    fin_affectation = fields.Date('Fin affectation')
    employee_id = fields.Many2one(comodel_name='hr.employee')
    structure_wizard_id = fields.Many2one(comodel_name='hr.department', string='Structure')
    asset = fields.Char()
    lieu_id = fields.Many2one(comodel_name='invest.endroit')
    cheak_stat = fields.Char()
    # type = fields.Selection([('affectation', 'Affectation'), ('finaffectation', 'Fin Affectation')])
    nom_wizard = fields.Char('Affectation Immobilisation')

    def name_get(self):
        result = []
        for record in self:
            nom_wizard = record.nom_wizard
            print('meba')
            print(nom_wizard)
            result.append((record.id, nom_wizard))
        return result

    @api.multi
    @api.onchange('employee_id')
    def get_structure_from_employee(self):
        for rec in self:
            if rec.employee_id:
                rec.structure_wizard_id = rec.employee_id.department_id.id


    @api.multi
    @api.onchange('structure_id')
    def get_employee_from_structure(self):

        for rec in self:
            domain = []
            team_ids = []
            if rec.structure_id:
                team_ids = self.env['hr.employee'].search(
                    [('department_id', '=', rec.structure_id.id)])
            if team_ids:
                domain.append(('id', 'in', team_ids.ids))
            else:
                domain = ''
        return {'domain': {'employee_id': domain}}


    def button_affectation(self):
        record1 = self.env['account.asset.asset'].browse(self._context['active_ids'])
        for rec in record1:
            if rec.state == 'draft':
                affectation(self,rec)
            else:
                reaffectation(self,rec)

def affectation(self,rec):
        # record = self.env['account.asset.asset'].browse(self._context['active_id'])
        record = self.env['account.asset.asset'].search([('id', '=', rec.id)])
        seq1 = self.env['account.asset.asset'].search(
            [('category_id', '=', record.category_id.id), ('state', '!=', 'draft')])
        for rec1 in record:
            account = rec1.env['account.account'].search([('id', '=', rec1.category_id.account_asset_id.id)])
            rec1.code = account.code
        config1 = record.env['res.config.settings'].sudo().create({})
        value1 = config1.my_config_value
        config1 = record.env['res.config.settings'].sudo().create({})
        value1 = config1.my_config_value

        if record.value >= float(value1):
            record.numero_inventaire = str(1) + '-' + record.code + '-' + str(len(seq1) + 1).zfill(4) + '-' + str(time.strftime('%Y')[-2]) + str(time.strftime('%Y')[-1])
        else:
            record.faible_valeur = True
            seqF = record.env['account.asset.asset'].search(
                [('faible_valeur', '=', True), ('annee', '=', time.strftime('%Y')), ('state', '!=', 'draft')])
            record.numero_inventaire = 'F' + '-' + str(len(seqF) + 1).zfill(4) + '-' + str(time.strftime('%Y')[-2]) + str(time.strftime('%Y')[-1])
        record.barcode_image = générer_code_barre(record)

        for rec in record:
            if rec.date < rec.date_aquisition:
                raise UserError("Date d'ammortissement doit être supérieur à la date d'aquisition")
            if rec.date_demande_achat:
                if rec.date_demande_achat > rec.date_aquisition:
                    raise UserError("Date demande achat doit être inférieur à la date d'aquisition")
            if rec.date_transfert:
                if rec.date_transfert < rec.date_aquisition:
                    raise UserError("Date aquisition doit être inférieur à la date transfert")

            affectation3 = self.env['invest.affectation'].search(
                [('asset_id', '=', rec.id)], limit=1, order='id desc')

            if affectation3:
                if affectation3.date_affectation >= self.date_affectation:
                    raise UserError("La date d'affectation doit supréieur à la fin de la dernière affectation ")

                affectation3.write({
                        'fin_affectation': fields.Datetime.now(),
                    })
                rec.affectation_id = None
                rec.endroit_id_1 = None
                rec.personnel_id = None
                rec.structure_id = None


            rec.endroit_id_1 = self.lieu_id.id
            rec.personnel_id = self.employee_id.id
            rec.structure_id = self.structure_wizard_id.id
            affectation = self.env['invest.affectation'].create({
                        'asset_id': rec.id,
                        'employee_id': self.employee_id.id,
                        'structure_id': self.structure_wizard_id.id,
                        'endroit_id': self.lieu_id.id,
                        'date_affectation': self.date_affectation
                    })

            rec.affectation_id = affectation.id
        if record.state == 'draft':
            record.write({'state': 'open'})
            fields = [
                'method',
                'method_number',
                'method_period',
                'method_end',
                'method_progress_factor',
                'method_time',
                'salvage_value',
                'invoice_id',
            ]
            ref_tracked_fields = self.env['account.asset.asset'].fields_get(fields)
            for asset in record:
                tracked_fields = ref_tracked_fields.copy()
                if asset.method == 'linear':
                    del (tracked_fields['method_progress_factor'])
                if asset.method_time != 'end':
                    del (tracked_fields['method_end'])
                else:
                    del (tracked_fields['method_number'])
                dummy, tracking_value_ids = asset._message_track(tracked_fields, dict.fromkeys(fields))
                asset.message_post(subject=_('Asset created'), tracking_value_ids=tracking_value_ids)


def reaffectation(self,rec):

            # record = self.env['account.asset.asset'].browse(self._context['active_id'])
            record = self.env['account.asset.asset'].search([('id', '=', rec.id)])

            for rec in record:
                affectation3 = self.env['invest.affectation'].search(
                    [('asset_id', '=', rec.id)], limit=1, order='id desc')

                if rec.state == 'close':
                    raise UserError("Vous ne pouvez pas affecter un bien réformer")

                if affectation3:
                    if affectation3.date_affectation >= self.date_affectation:
                        raise UserError("La date d'affectation doit supréieur à la fin de la dernière affectation ")


                    affectation3.write({
                        'fin_affectation': self.date_affectation,
                    })
                    rec.affectation_id = None
                    rec.endroit_id_1 = None
                    rec.personnel_id = None
                    rec.structure_id = None

                rec.endroit_id_1 = self.lieu_id.id
                rec.personnel_id = self.employee_id.id
                rec.structure_id = self.structure_wizard_id.id
                affectation = self.env['invest.affectation'].create({
                    'asset_id': rec.id,
                    'employee_id': self.employee_id.id,
                    'structure_id': self.structure_wizard_id.id,
                    'endroit_id': self.lieu_id.id,
                    'date_affectation': self.date_affectation
                })

                rec.affectation_id = affectation.id


