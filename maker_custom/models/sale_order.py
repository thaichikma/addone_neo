from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_quotation_date = fields.Datetime("Quotation Date", default=fields.Datetime.now, copy=False)
    x_validity_day = fields.Integer("Validity (days)", copy=False)
    x_lead_time = fields.Integer("Lead-Time (weeks)", copy=False)

    x_partner_child_ids = fields.One2many(related="partner_id.child_ids")
    x_contact_id = fields.Many2one('res.partner',  String='Contact')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_product_maker = fields.Many2one("xres.maker", "Maker", related="product_id.x_maker", store=True, copy=False)
    x_product_model = fields.Char("Model", related="product_id.x_model", store=True, copy=False)

    # @api.onchange('product_id')
    # def _onchange_get_maker_model(self):
    #     if self.product_id:
    #         self.x_product_maker = self.product_id.x_maker
    #         self.x_product_model = self.product_id.x_model
