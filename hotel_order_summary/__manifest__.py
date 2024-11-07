{
    'name': 'Hotel Order Summary ',
    'version': '16',
    'author': 'Febno',
    'category': '',
    'description': """ Order Summary from folio for the customer """,
    'depends': ['base','sale','hotel_management','banquet_managment','hotel','web'],
    'license': 'OPL-1',
    "currency": "",

    'data': [
        'report/order_summary_template.xml',
        'report/report.xml'
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
