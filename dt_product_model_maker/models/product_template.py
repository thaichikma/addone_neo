# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    maker_id = fields.Many2one('nihon.maker', 'Maker', copy=False)
    nihon_model = fields.Char('Model', copy=False)

    _sql_constraints = [
        ('code_uniq', 'unique (maker_id, nihon_model)', "Duplicate maker and model"),
    ]
    # @api.constrains('maker_id', 'nihon_model')
    # def check_name(self):
    #     domain = [('maker_id', '=', self.maker_id.id),
    #               ('nihon_model', '=ilike', self.nihon_model)]
    #
    #     products = self.env['product.template'].sudo().search(domain)
    #
    #     if len(products) > 1:
    #         raise ValidationError(_('Error ! Model and Maker are duplicated'))

