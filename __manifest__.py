# -*- coding: utf-8 -*-
{
    'name'     : 'InfoSaône - Module Odoo pour IECS',
    'version'  : '0.1',
    'author'   : 'InfoSaône',
    'category' : 'InfoSaône',
    'description': """
InfoSaône - Module Odoo pour IECS
===================================================
""",
    'maintainer' : 'InfoSaône',
    'website'    : 'http://www.infosaone.com',
    'depends'    : [
        'base',
        'base_vat',
        'account',
        'l10n_fr',
        'sale',
        'sale_management',
        'purchase',
        'stock',
        'document',
        'product',
        'board',
    ],
    'data' : [
        'security/ir.model.access.csv',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'views/sale_views.xml',
        'views/is_tresorerie_views.xml',
        'views/is_affaire_view.xml',
        'views/purchase_view.xml',
        'views/menu.xml',
        'report/report_templates.xml',
        'report/purchase_order_templates.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
    ],
}

