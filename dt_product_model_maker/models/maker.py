from odoo import fields, models, api


class MakerModel(models.Model):
    _name = 'nihon.maker'
    _description = 'Maker'

    name = fields.Char()
