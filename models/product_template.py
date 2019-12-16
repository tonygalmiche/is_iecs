# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_type_article = fields.Selection([
            ('standard'            , 'Standard'),
            ('avec-numero-de-serie', "Avec numéro de série et garantie"),
            ('machine'             , 'Machine'),
        ], u"Famille d'article",default='standard',required=True,index=True)
    is_num_serie      = fields.Char("Numéro de série")
    is_garantie       = fields.Date("Garantie")
    is_certificat_ce  = fields.Char("Certificat CE")
    is_piece_rechange = fields.Boolean("Pièces de rechange")

