from odoo import models, fields, api, _


from odoo.exceptions import UserError


class AccountAssetDepreciationLigneInherited(models.Model):
    _inherit = "account.asset.depreciation.line"

    affectation_ids = fields.One2many(comodel_name='invest.affectation', inverse_name='employee_id')

    # @api.one
    # def unlink(self):
    #     print('hhhhh')
    #
    #     raise UserError("You cannot delete depreciation line IDs.")


