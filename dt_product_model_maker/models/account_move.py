from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    maker_id = fields.Many2one(string="Maker", comodel_name='nihon.maker', related='product_id.maker_id')
    nihon_model = fields.Char(string="Model", related='product_id.nihon_model')

    # @api.depends('product_id')
    # def _compute_maker_id(self):
    #     for line in self:
    #         line.maker_id = line.product_id.maker_id

    # @api.depends('product_id')
    # def _compute_model(self):
    #     for line in self:
    #         line.nihon_model = line.product_id.nihon_model
