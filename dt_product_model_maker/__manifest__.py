# -*- coding: utf-8 -*-
{
    'name': "product_model_maker",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'sequence': -100,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'sale', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/purchase_order_view.xml',
        'views/stock_picking_view.xml',
        'views/account_move_view.xml',
        'views/product_product_view.xml',
        'views/sale_order_view.xml',
        'report/report.xml',
        'report/report_templates_inherit.xml',
        'report/quotation_report.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            '/dt_product_model_maker/static/scss/custom_font.scss'
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
