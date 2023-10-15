from odoo import models, fields, api, _


class HrJobInherited(models.Model):
    _inherit = "hr.job"