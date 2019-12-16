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
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'views/sale_views.xml',
        'views/is_tresorerie_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
    ],
}

