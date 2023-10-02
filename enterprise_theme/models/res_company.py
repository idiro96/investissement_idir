# -*- coding: utf-8 -*-
"""Adds functionality to res.company"""
from odoo import api, fields, models
from odoo.modules.module import get_module_resource
import base64
from odoo import tools, _


class ResCompany(models.Model):
    """Model res.company"""
    # pylint: disable=too-few-public-methods

    _inherit = 'res.company'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('enterprise_theme', 'static/src/img', 'dashboard.jpg')
        return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))
    background_image = fields.Binary(default=_default_image,attachment=True)

    background_allow_users = fields.Boolean(
        string="Allow users to set custom background images"
    )

    dashboard_logo = fields.Boolean(default=True,
                                    string="Show company logo on dashboard")
