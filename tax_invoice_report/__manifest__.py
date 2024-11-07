
{
    'name': 'Tax Invoice',
    'version': '16.0.1.0.0',
    'description': "Report",
    'author': 'Febno',
    'company': 'Febno',
    'website': '',
    'depends': ['base', 'account', 'sale'],
    'data': [
        # 'reports/report_iv.xml',
        'reports/tax_report_template.xml',
        'reports/report.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}
