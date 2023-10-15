from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountAssetCategorieInherited(models.Model):
    _inherit = "account.asset.category"

    ammortissement_ligne2_ids = fields.One2many(comodel_name='invest.ammortissement.matricielle', inverse_name='categorie_id')

    method_number = fields.Integer(default=0)
    method_period = fields.Integer(default=12)
    product_id_1 = fields.Many2one('product.template')

    sous_compte_ligne_ids = fields.One2many(comodel_name='invest.sous.compte.asset', inverse_name='compte')
    account_asset_id = fields.Many2one('account.account', string='Asset Account', required=True, domain=[('internal_type','=','other'), ('deprecated', '=', False)], help="Account used to record the purchase of the asset at its original price.")

    @api.multi
    @api.onchange('account_asset_id')
    def sous_compte_ligne(self):
        records = self.env['invest.sous.compte.asset'].search([('compte.id', '=', self.account_asset_id.id)])
        self.sous_compte_ligne_ids = records


    @api.onchange('method')
    def ammortissement_ligne(self):
        """Dans cette wizard on insere le plan d'aommortissement de bien immobilier"""
        model = self.env['ammortissement.ligne']
        records = model.search([])
        records.unlink()

        return {
        'type': 'ir.actions.act_window',
        'target': 'new',
        'name': 'Ammortissement',
        'view_mode': 'form',
        'res_model': 'ammortissement.ligne',
       }


