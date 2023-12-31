# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2019 GRIMMETTE,LLC <info@grimmette.com>

{
    'name': 'Report Designer (XLSX, XLSM)',
    'version': '1.3.21',
    'category': 'Extra Tools',
    'summary': 'Report Designer allows to Create and Print various Financial and Analytical reports in MS Excel format (XLSX, XLSM)',
    'price': 299.00,
    'currency': 'EUR',
    "license": "OPL-1",
    'description': """
Report Designer for Odoo.
====================================
Design various Reports and Print Reports in MS Excel format (XLSX)
Generate the Excel Report from a Template.
Report Excel Designer for Odoo. 
    Odoo Report XLSX  Create Excel Report Excel Reports Accounting Reports Financial Report Financial Reports Stock Reports Inventory Reports \
    Dynamic Sale Analysis Reports Export Excel Export xlsx Project Reports Warehouse Reports Purchases Reports Marketing Reports Sales Reports \
    Report Designer Reports Designer Report Builder Reports Builder Product Report Customer Report POS Reports POS Report Analysis Report \
    BI Report BI Reports BI Business Intelligence Report Business Intelligence Reports BI Analytics BI Analytic Data Analysis Reporting Tool
    """,
    'author': 'GRIMMETTE',
    'support': 'info@grimmette.com',
    'depends': ['base','web','attachment_indexation','mail','base_sparse_field'],
    'images': ['static/description/reports.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/report_excel_views.xml',
        'views/menuitem.xml',
        # 'static/src/xml/assets.xml',
        'data/ir_sequence_data.xml',
        'data/aggregate_data.xml',
        'wizard/report_excel_wizard_view.xml',
        'wizard/report_excel_export_import_wizard_view.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'report_excel/static/src/js/*.js',
            'report_excel/static/src/css/*.css',
            'report_excel/static/src/xml/*.xml',
        ],
    },

    # 'qweb': [
    #     'static/src/xml/templates.xml',
    # ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    # "pre_init_hook": "pre_init_check",
}
