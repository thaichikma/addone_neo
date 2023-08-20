# -*- coding: utf-8 -*-
from odoo import models, _, fields



class ResCompany(models.Model):

    _inherit = "res.company"

    x_qr_code = fields.Binary(string='Image QR')
