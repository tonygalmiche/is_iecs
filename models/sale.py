# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = "sale.order.line"

    is_puissance = fields.Float(u"Puissance (KW)")
    is_poids     = fields.Float(u"Poids (Kg)")
    is_container = fields.Float(u"Container 40 pieds")
