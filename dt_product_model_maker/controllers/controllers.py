# -*- coding: utf-8 -*-
# from odoo import http


# class DtProductModelMaker(http.Controller):
#     @http.route('/dt_product_model_maker/dt_product_model_maker', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dt_product_model_maker/dt_product_model_maker/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dt_product_model_maker.listing', {
#             'root': '/dt_product_model_maker/dt_product_model_maker',
#             'objects': http.request.env['dt_product_model_maker.dt_product_model_maker'].search([]),
#         })

#     @http.route('/dt_product_model_maker/dt_product_model_maker/objects/<model("dt_product_model_maker.dt_product_model_maker"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dt_product_model_maker.object', {
#             'object': obj
#         })
