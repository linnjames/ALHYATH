
{
    'name': 'Currency Exchange',
    'version': '16.0.1.0.0',
    'description': "Guests can exchange their currency from hotel",
    'author': 'Febno',
    'company': 'Febno',
    'website': '',
    'depends': ['base', 'account', 'sale','hotel_management','hotel','hotel_restaurant'],
    'data': [
        'data/data.xml',
        'views/currency_exchange_journal.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}
