{
    'name': 'Settlement Report',
    'summary': """Hotel Management Settlement Report """,
    'version': '16',
    'author': 'Febno',
    'category': '',
    'description': """""",
    'depends': ['base','account','sale','hotel_management','banquet_managment','report_xlsx'],
    'license': 'OPL-1',
    "currency": "",

    'data': [
        'security/ir.model.access.csv',
        'wizard/revenue_report.xml',
        'wizard/daywise_report.xml',
        'report/report.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
