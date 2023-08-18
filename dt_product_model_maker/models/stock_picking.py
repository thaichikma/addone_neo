from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'stock.move.line'

    maker_id = fields.Many2one(string="Maker", comodel_name='nihon.maker', related='product_id.maker_id')
    nihon_model = fields.Char(string="Model", related='product_id.nihon_model')
