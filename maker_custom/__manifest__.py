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
    'depends': ['base', 'product', 'sale', 'sale_stock',
                'purchase', 'account', 'stock',
                'payment',
                'report_xlsx','sale_management'],
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
        'wizard/report.xml',
        # 'views/sale_stock_views.xml',
    ],
    "assets": {

    },
    'images': ['images/contact.png',
               'images/email.png',
               'images/addess.png',
               'images/company.png',
               'images/icon_position.png',
               'images/phone.png',
               'images/logo.png',
               'images/logo1.png',
               'images/logo2.png',
               'images/logo3.png',
               'images/signature.png',
                'images/logoinfo.png',
                'images/logoneo.png',

               ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
