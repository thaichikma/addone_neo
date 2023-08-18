from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_partner_child_ids = fields.One2many(related="partner_id.child_ids")
    x_contact_id = fields.Many2one('res.partner',  String='Contact')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_product_maker = fields.Many2one("xres.maker", "Maker", related="product_id.x_maker", store=True, copy=False)
    x_product_model = fields.Char("Model", related="product_id.x_model", store=True, copy=False)

    # @api.onchange('product_id')
    # def _onchange_get_maker_model(self):
    #     if self.product_id:
    #         self.x_product_maker = self.product_id.x_maker
    #         self.x_product_model = self.product_id.x_model


