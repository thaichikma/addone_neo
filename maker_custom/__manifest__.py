# -*- coding: utf-8 -*-
{
    'name': "Model Maker Custom",

    'summary': """""",

    'description': """
        
    """,

    'author': "******",
    'website': "******",

    "category": "",
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale', 'sale_stock', 'purchase', 'account', 'stock'],
    # 'auto_install': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        # DATA
        # 'data/ir_sequence_data.xml',
        # Views


        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_move_views.xml',
        'views/account_move_views.xml',
        # 'views/sale_stock_views.xml',
    ],
    "assets": {

    },
    # only loaded in demonstration mode
    'demo': [
    ],
}
