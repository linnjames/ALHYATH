# -*- coding: utf-8 -*-
{
    'name': 'Base Reports',
    'version': '16.0.1.0',
    'category': 'Reports',
    'author': 'Febno',
    'website': "",
    'description': """
        -Invoice and sales reports.
    """,
    'depends': ['base','account','sale','base_accounting_kit'],
    'data': [
        "views/res_company_view.xml",
        "wizard/account_partner_ledger_view.xml",
        "reports/report_invoice_inherit.xml",
        "reports/report_partner_ledger_inherit.xml",
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}