# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_presentation = fields.Char("Présentation")
    is_capital      = fields.Char("Capital")

