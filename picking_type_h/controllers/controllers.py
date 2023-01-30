# -*- coding: utf-8 -*-
# from odoo import http


# class PointSale(http.Controller):
#     @http.route('/point_sale/point_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/point_sale/point_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('point_sale.listing', {
#             'root': '/point_sale/point_sale',
#             'objects': http.request.env['point_sale.point_sale'].search([]),
#         })

#     @http.route('/point_sale/point_sale/objects/<model("point_sale.point_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('point_sale.object', {
#             'object': obj
#         })
