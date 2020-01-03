# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta


class IsMatiere(models.Model):
    _name = 'is.matiere'
    _description = "Matière"
    _order = 'name'

    name = fields.Char("Matière", required=True, index=True)


class ProductTemplate(models.Model):
    _inherit = "product.template"


    @api.depends('is_date_depart_garantie','is_duree_garantie')
    def _compute_is_date_fin_garantie(self):
        for obj in self:
            date = False
            if obj.is_date_depart_garantie:
                date = obj.is_date_depart_garantie + relativedelta(months=+obj.is_duree_garantie)
            obj.is_date_fin_garantie = date

    is_type_article = fields.Selection([
            ('standard'            , 'Standard'),
            ('avec-numero-de-serie', "Avec numéro de série et garantie"),
            ('machine'             , 'Machine'),
            ('outillage'           , 'Outillage'),
        ], u"Famille d'article",default='standard',required=True,index=True)
    is_num_serie            = fields.Char("Numéro de série")
    is_date_depart_garantie = fields.Date(u"Début garantie")
    is_duree_garantie       = fields.Integer(u"Durée garantie")
    is_date_fin_garantie    = fields.Date(u"Fin de garantie", compute='_compute_is_date_fin_garantie', readonly=True, store=True)
    is_certificat_ce_ids    = fields.Many2many('ir.attachment', 'product_template_certificat_ce_rel', 'product_id', 'file_id', 'Certificat CE')
    is_plan_ids             = fields.Many2many('ir.attachment', 'product_template_plan_rel'         , 'product_id', 'file_id', 'Plans')
    is_photo_ids            = fields.Many2many('ir.attachment', 'product_template_photo_rel'        , 'product_id', 'file_id', 'Photos')
    is_notice_ids           = fields.Many2many('ir.attachment', 'product_template_notice_rel'       , 'product_id', 'file_id', 'Notices')
    is_piece_rechange       = fields.Boolean("Pièces de rechange")
    is_matiere_id           = fields.Many2one('is.matiere', u"Matière")
    is_emplacement_stock_id = fields.Many2one('stock.location', u"Emplacement", domain=[('usage','=','internal')])
    is_puissance            = fields.Float(u"Puissance (KW)")
    is_largeur_tapis        = fields.Integer(u"Largeur tapis")
    is_marque               = fields.Char("Marque")
    is_modele               = fields.Char("Modèle")
