from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    maker_id = fields.Many2one(string="Maker", comodel_name='nihon.maker', compute='_compute_maker_id')
    nihon_model = fields.Char(string="Model", compute='_compute_model')

    @api.depends('product_tmpl_id')
    def _compute_maker_id(self):
        for line in self:
            line.maker_id = line.product_tmpl_id.maker_id

    @api.depends('product_tmpl_id')
    def _compute_model(self):
        for line in self:
            line.nihon_model = line.product_tmpl_id.nihon_model
