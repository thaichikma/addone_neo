from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = 'account.move.line'

    x_product_maker = fields.Many2one("xres.maker", "Maker", copy=False)
    x_product_model = fields.Char("Model", copy=False)

    @api.onchange('product_id')
    def _onchange_get_maker_model(self):
        if self.product_id:
            self.x_product_maker = self.product_id.x_maker
            self.x_product_model = self.product_id.x_model
