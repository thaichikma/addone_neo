from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_maker = fields.Many2one("xres.maker", "Maker", copy=False)
    x_model = fields.Char("Model",copy=False)
    x_name_description = fields.Html(compute="_compute_name_description", store=True)


    @api.constrains('x_model','x_maker')
    def validate_model_maker(self):

        domain = [('x_model', '=ilike', self.x_model)]

        if self.x_maker:
            domain.append(('x_maker', 'in', self.x_maker.ids))
        else:
            domain.append(('x_maker', '=', False))

        product = self.env['product.template'].sudo().search(domain, limit=2)

        if len(product) > 1:
            raise ValidationError(_('Error ! Model and Maker are duplicated'))

        return True

    @api.depends('name', 'description')
    def _compute_name_description(self):
        for line in self:
            if line.name or line.description:
                line.x_name_description = f'<p>{line.name or ""}</p><p>{line.description or ""}</p>'
            else:
                line.x_name_description = ""


class XResMarker(models.Model):
    _name = 'xres.maker'
    rec_name = 'name'

    name = fields.Char('Maker')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'A maker with this name already exists!')
    ]
