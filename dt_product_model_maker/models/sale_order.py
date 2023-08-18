from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contact_id = fields.Many2one(
        comodel_name='res.partner',
        string="Contact",
        domain="[('parent_id', '!=', False)]")
    validity_days = fields.Integer(string="Validity Days")
    lead_time = fields.Integer(string="Lead-Time")

    @api.onchange('partner_id')
    def get_contact(self):
        return {'domain': {'contact_id': [('parent_id', '=', self.partner_id.id)]}}

    def print_quotation(self):
        return self.env.ref('dt_product_model_maker.action_print_quotation').report_action(self)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    maker_id = fields.Many2one(string="Maker", comodel_name='nihon.maker', related='product_id.maker_id')
    nihon_model = fields.Char(string="Model", related='product_id.nihon_model')
