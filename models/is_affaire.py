# -*- coding: utf-8 -*-
from openerp import models,fields,api
import datetime


class is_affaire(models.Model):
    _name='is.affaire'
    _description = "Affaire"
    _order='name'

    name              = fields.Char(u"Affaire", required=True)
    location_id       = fields.Many2one('stock.location', u'Emplacement de stock', domain=[('usage','=','internal')])
    client_id         = fields.Many2one('res.partner', u'Client', domain=[('is_company','=',True),('customer','=',True)], required=True)
    chef_projet       = fields.Char(u"Chef de projet")
    commentaire       = fields.Text(u"Commentaire")
    sous_ensemble_ids = fields.One2many('is.sous.ensemble', 'affaire_id', u'Sous-ensembles', readonly=False)


    @api.model
    def create(self, vals):
        location = self._creer_emplacement_stock(vals['name'])
        vals['location_id']=location.id
        obj = super(is_affaire, self).create(vals)
        return obj


    @api.multi
    def write(self,vals):
        for obj in self:
            if 'name' in vals and obj.location_id:
                obj.location_id.name = vals['name']
        res = super(is_affaire, self).write(vals)
        return res


    @api.multi
    def _creer_emplacement_stock(self,name):
        locations = self.env['stock.location'].search([('name','=',name)])
        if len(locations):
            location = locations[0]
        else:
            vals={
                'location_id': 3, # Emplacements Virtuels
                'name'       : name,
                'usage'      : 'internal',
            }
            location = self.env['stock.location'].create(vals)
        return location


    @api.multi
    def creer_emplacement_stock_action(self):
        for obj in self:
            if not obj.location_id:
                location = self._creer_emplacement_stock(obj.name)
                obj.location_id = location.id





class is_sous_ensemble(models.Model):
    _name='is.sous.ensemble'
    _description = "Sous-ensemble"
    _order='name'

    name        = fields.Char(u"Sous-ensemble", required=True)
    affaire_id  = fields.Many2one('is.affaire', u'Affaire', required=True)


    @api.multi
    def acceder_sous_ensemble(self):
        for obj in self:
            return {
                'name': u'Sous-ensemble '+obj.name or '',
                'view_mode': 'form,tree',
                'view_type': 'form',
                'res_model': 'is.sous.ensemble',
                'res_id': obj.id,
                'type': 'ir.actions.act_window',
            }


    @api.multi
    def acceder_lignes(self):
        for obj in self:
            return {
                'name': "Lignes",
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'is.sous.ensemble.line',
                'type': 'ir.actions.act_window',
                'domain': [('sous_ensemble_id','=',obj.id)],
                'context': {
                    'default_sous_ensemble_id': obj.id,
                    'default_affaire_id'      : obj.affaire_id.id,
                },
                'limit': 200,
            }



class is_sous_ensemble_line(models.Model):
    _name='is.sous.ensemble.line'
    _description = "Sous-Ensemble - Ligne"
    _order='affaire_id,sous_ensemble_id,ordre,product_id'
    _rec_name='product_id'


    affaire_id           = fields.Many2one('is.affaire',u'Affaire', required=True)
    sous_ensemble_id     = fields.Many2one('is.sous.ensemble', u'Sous-ensemble', required=True)
    ordre                = fields.Integer(u"Ligne")
    product_id           = fields.Many2one('product.product', u'Article', domain=[('purchase_ok', '=', True)])
    #reference            = fields.Char(u'Référence', readonly=True)
    #designation          = fields.Char(u'Désignation', readonly=True)
    #creation_product     = fields.Boolean(u"Création",help=u"Indique si l'article a été créé lors de l'importation",readonly=True)
    #matiere_id           = fields.Many2one('is.matiere', u'Matière')
    #fabriquant           = fields.Char(u"Fabriquant")
    quantite             = fields.Integer(u"Quantité")
    #categorie_article_id = fields.Many2one('is.categorie.article', u'Catégorie')
    #suivi_par_id         = fields.Many2one('res.users', u'Suivi par')
    order_id             = fields.Many2one('purchase.order', u'N°Cde', copy=False)
    date_cde             = fields.Date(u"Date Cde", copy=False)
    delai                = fields.Date(u"Délai", copy=False)
    recu_le              = fields.Date(u"Reçu le", copy=False)
    #code                 = fields.Char(u"Code Fournisseur")
    fournisseur_id       = fields.Many2one('res.partner', u'Fournisseur', domain=[('is_company','=',True),('supplier','=',True)], copy=False)
    ref_fournisseur      = fields.Char(u"Réf fournisseur", copy=False)
    pu_ht                = fields.Float(u"PU HT", copy=False)
    total_ht             = fields.Float(u"Total HT", copy=False)
    order_ids            = fields.Many2many('purchase.order', 'is_sous_ensemble_line_order_rel', 'line_id','order_id', string=u"Devis", copy=False)
    order_nb             = fields.Integer(u"Nb devis", copy=False)
    #anomalie             = fields.Char(u"Anomalie")
    order_line_ids       = fields.One2many('is.sous.ensemble.line.order', 'line_id', u'Lignes de commandes', readonly=True, copy=False)


    @api.multi
    def creer_devis_action(self):
        affaire_id = False
        for obj in self:
            affaire_id=obj.affaire_id.id
        user = self.env['res.users'].search([('id','=',self._uid)],limit=1)[0]
        partner = user.partner_id
        vals={
            'partner_id'        : partner.id,
            'is_affaire_id'     : affaire_id,
            'fiscal_position_id': partner.property_account_position_id.id,
        }
        order=self.env['purchase.order'].create(vals)
        if order:
            order_line_obj = self.env['purchase.order.line']
            for obj in self:
                now = datetime.date.today()
                date_planned = now.strftime('%Y-%m-%d')
                obj.suivi_par_id = self._uid
                taxes_id=[]
                for tax in obj.product_id.supplier_taxes_id:
                    taxes_id.append(tax.id)
                vals={
                    'order_id'      : order.id,
                    'product_id'    : obj.product_id.id,
                    'name'          : obj.product_id.name,
                    'is_affaire_id' : obj.affaire_id.id,
                    'product_uom'   : obj.product_id.uom_id.id ,
                    'price_unit'    : 0,
                    'product_qty'   : obj.quantite,
                    'date_planned'  : date_planned,
                    'taxes_id'      : [(6,0,taxes_id)],
                }
                line=order_line_obj.create(vals)
                obj.actualiser()


    @api.multi
    def actualiser_ligne_scheduler_action(self):
        self.env['is.sous.ensemble.line'].search([]).actualiser_ligne_action()


    @api.multi
    def actualiser_ligne_action(self):
        nb=len(self)
        ct=0
        for obj in self:
            ct+=1
            obj.actualiser()


    @api.multi
    def actualiser(self):
        for obj in self:
            obj.order_line_ids.unlink()
            #obj.reference            = obj.product_id.default_code
            #obj.designation          = obj.product_id.name
            #obj.matiere_id           = obj.product_id.is_matiere_id
            #obj.fabriquant           = obj.product_id.is_fabriquant
            #obj.categorie_article_id = obj.product_id.is_categorie_article_id
            lines = self.env['purchase.order.line'].search([('product_id','=',obj.product_id.id)],order="id desc",limit=20)
            nb=0
            for line in lines:
                nb+=1
                vals={
                    'affaire_id'      : obj.affaire_id.id,
                    'sous_ensemble_id': obj.sous_ensemble_id.id,
                    'line_id'         : obj.id,
                    'order_id'        : line.order_id.id,
                    'partner_id'      : line.partner_id.id,
                    'product_id'      : line.product_id.id,
                    'quantite'        : line.product_qty,
                    'prix'            : line.price_unit,
                    'state'           : line.order_id.state,
                }
                if line.order_id.state=='purchase' and line.is_affaire_id==obj.affaire_id:
                    obj.order_id        = line.order_id.id
                    obj.fournisseur_id  = line.order_id.partner_id.id
                    obj.pu_ht           = line.price_unit
                    obj.total_ht        = line.price_subtotal
                    for move in line.move_ids:
                        if move.state=='done':
                            obj.recu_le=move.date
                line=self.env['is.sous.ensemble.line.order'].create(vals)
            obj.order_nb = nb


class is_sous_ensemble_line_order(models.Model):
    _name='is.sous.ensemble.line.order'
    _description = "Sous-Ensemble - Commande"

    affaire_id           = fields.Many2one('is.affaire',u'Affaire', required=True)
    sous_ensemble_id     = fields.Many2one('is.sous.ensemble', u'Sous-ensemble', required=True)
    line_id              = fields.Many2one('is.sous.ensemble.line', u'Ligne', required=True, ondelete='cascade')
    order_id             = fields.Many2one('purchase.order', u'Commande')
    partner_id           = fields.Many2one('res.partner', u'Fournisseur')
    product_id           = fields.Many2one('product.product', u'Référence')
    quantite             = fields.Float(u"Quantité")
    prix                 = fields.Float(u"PU HT")
    state                = fields.Char(u"Etat")






