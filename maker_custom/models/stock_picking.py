from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime



class StockPicking(models.Model):

    _inherit = 'stock.picking'

    def print_excel(self):
        action = self.env.ref('maker_custom.delivery_print_excel_in_report').read()[0]
        return action

    def print_excel_packing(self):
        action = self.env.ref('maker_custom.packing_print_excel_in_report').read()[0]
        return action

    def lay_ngay_hien_tai(self):
        ngay_hien_tai = datetime.now().strftime('%d_%m_%Y')
        return ngay_hien_tai
