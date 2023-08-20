from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime


class StockMoveLine(models.Model):
    _inherit = 'account.move.line'

    x_product_maker = fields.Many2one("xres.maker", "Maker", copy=False)
    x_product_model = fields.Char("Model", copy=False)

    @api.onchange('product_id')
    def _onchange_get_maker_model(self):
        if self.product_id:
            self.x_product_maker = self.product_id.x_maker
            self.x_product_model = self.product_id.x_model

    def print_excel(self):
        action = self.env.ref('maker_custom.ms_report_account_print_excel_report').read()[0]
        return action
    def lay_ngay_hien_tai(self):
        ngay_hien_tai = datetime.now().strftime('%d_%m_%Y')
        return ngay_hien_tai