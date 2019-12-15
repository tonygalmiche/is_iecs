# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from datetime import date,timedelta
import random


class IsTresorerie(models.Model):
    _name = 'is.tresorerie'
    _description = "Trésorerie"
    _order = 'date_creation desc'
    _rec_name = 'date_creation'

    date_creation = fields.Date("Date de création", readonly=True, index=True, default=lambda *a: fields.Date.today())
    solde_depart  = fields.Float("Solde de départ", required=True)
    nb_jours      = fields.Integer("Nombre de jours", required=True, default=28)
    line_ids      = fields.One2many('is.tresorerie.line', 'tresorerie_id', u'Dates')


    @api.multi
    def calculer_tresorerie(self):
        for obj in self:
            obj.line_ids.unlink()
            jour = date.today()
            for i in range(0,obj.nb_jours):
                solde = 10000.0*(random.random()-0.2)
                solde_debit = 0
                solde_credit = 0
                if solde<0:
                    solde_debit=solde
                    etat = 'debit'
                else:
                    solde_credit = solde
                    etat = 'credit'
                vals={
                    'tresorerie_id': obj.id,
                    'jour'         : jour,
                    'etat'         : etat,
                    'solde'        : solde,
                    'solde_debit'  : solde_debit,
                    'solde_credit' : solde_credit,
                }
                res=self.env['is.tresorerie.line'].create(vals)
                jour = jour + timedelta(days=1)
            tree_view  = self.env.ref('is_iecs.is_tresorerie_line_tree', False)
            graph_view = self.env.ref('is_iecs.is_tresorerie_line_graph', False)
            pivot_view = self.env.ref('is_iecs.is_tresorerie_line_pivot', False)
            res= {
                'name': 'Trésorerie',
                #'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'is.tresorerie.line',
                'views': [(graph_view.id, 'graph'),(pivot_view.id, 'pivot'),(tree_view.id, 'tree')],
                'type': 'ir.actions.act_window',
                'domain' : [('tresorerie_id','=',obj.id)],
            }
            return res






class IsTresorerieLine(models.Model):
    _name = 'is.tresorerie.line'
    _description = "Trésorerie - Lignes"
    _order = 'jour'
    _rec_name = 'jour'

    tresorerie_id = fields.Many2one('is.tresorerie', 'Trésorerie', required=True, ondelete='cascade')
    jour          = fields.Date("Jour", required=True, index=True)
    etat = fields.Selection([
            ('debit' , u'Débit'),
            ('credit', u'Crédit'),
        ], u"État")
    solde        = fields.Float("Solde")
    solde_credit = fields.Float("Solde au crédit")
    solde_debit  = fields.Float("Solde au débit")






