from odoo import models, fields, api, _

class ConfigSettingsInherited(models.TransientModel):
    _inherit = 'res.config.settings'

    my_config_value = fields.Char(
        string='My Configuration Value',
    )

    @api.model
    def get_values(self):
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        return {
            'my_config_value': IrConfigParam.get_param('invest.my_config_value'),
        }

    def set_values(self):
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        IrConfigParam.set_param('invest.my_config_value', self.my_config_value)