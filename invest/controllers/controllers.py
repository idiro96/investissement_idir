# -*- coding: utf-8 -*-
from odoo import http

# class Invest(http.Controller):
#     @http.route('/invest/invest/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invest/invest/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invest.listing', {
#             'root': '/invest/invest',
#             'objects': http.request.env['invest.invest'].search([]),
#         })

#     @http.route('/invest/invest/objects/<model("invest.invest"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invest.object', {
#             'object': obj
#         })