from odoo import models, fields, api, _


class HrEmployeInherited(models.Model):
    _inherit = "hr.employee"

    asset_ids = fields.One2many(comodel_name='account.asset.asset', inverse_name='personnel_id')
    maintenance_ligne_ids = fields.One2many(comodel_name='invest.maintenance.ligne', inverse_name='personnel_id')
