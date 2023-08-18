from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer")

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    maker_id = fields.Many2one(string="Maker", comodel_name='nihon.maker', related='product_id.maker_id')
    nihon_model = fields.Char(string="Model", related='product_id.nihon_model')
