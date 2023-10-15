# -*- coding: utf-8 -*-

from odoo import models, fields, api


class invistissementMaintenanceAsset(models.TransientModel):
    _name = 'maintenance.asset'

    date_operation = fields.Date()
    service_fait = fields.Char()
    montant = fields.Float()
    piece_comptable = fields.Char()
    personnel_id = fields.Many2one(comodel_name='hr.employee')
    type_operation_id = fields.Many2one(comodel_name='invest.type.operation')

    def button_maintenance(self):
        record = self.env['account.asset.asset'].browse(self._context['active_id'])
        # record.write({'endroit_id_1': self.lieu_id.id})
        # record.write({'personnel_id': self.employee_id.id})

        maintenance = self.env['invest.maintenance.ligne'].create({
            'asset_id': record.id,
            'employee_id': self.personnel_id.id,
            'type_operation_id': self.type_operation_id.id,
            'date_operation': self.date_operation,
            'montant': self.montant,
            'piece_comptable': self.piece_comptable,
        })
        #
        # self.env['account.asset.asset'].create({
        #     'endroit_id_1': self.lieu_id.parent_id.id,
        #     # 'employee_id': self.employee_id.id,
        #     # 'endroit_id': self.lieu_id.id,
        #     # 'date_affectation': self.date_affectation
        # })

