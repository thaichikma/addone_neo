from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    x_product_maker = fields.Many2one("xres.maker", "Maker", compute="_compute_get_maker_model", store=True, copy=False)
    x_product_model = fields.Char("Model", store=True, compute="_compute_get_maker_model", copy=False)

    # @api.onchange('product_id')
    # def _onchange_get_maker_model(self):
    #     if self.product_id:
    #         self.x_product_maker = self.product_id.x_maker
    #         self.x_product_model = self.product_id.x_model

    @api.depends('product_id')
    def _compute_get_maker_model(self):
        for rec in self:
            if rec.product_id:
                rec.x_product_maker = rec.product_id.x_maker
                rec.x_product_model = rec.product_id.x_model
