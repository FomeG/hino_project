# -*- coding: utf-8 -*-
# from odoo import http


# class Banggia(http.Controller):
#     @http.route('/banggia/banggia', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/banggia/banggia/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('banggia.listing', {
#             'root': '/banggia/banggia',
#             'objects': http.request.env['banggia.banggia'].search([]),
#         })

#     @http.route('/banggia/banggia/objects/<model("banggia.banggia"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('banggia.object', {
#             'object': obj
#         })

