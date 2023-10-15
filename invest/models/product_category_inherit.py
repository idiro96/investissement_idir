from odoo import models, fields, api

class ProductCategoryInherited(models.Model):

    _inherit = "product.category"

    # categ_asset = fields.Many2one(comodel_name='account.asset.category')