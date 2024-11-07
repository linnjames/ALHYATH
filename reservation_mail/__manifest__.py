{
    'name': 'Reservation Confirmation Mail ',
    'summary': """ Sent a mail to the customer after room reservation  """,
    'version': '16',
    'author': 'Febno',
    'category': '',
    'description': """""",
    'depends': ['base','sale','hotel_management','banquet_managment'],
    'license': 'OPL-1',
    "currency": "",

    'data': [
        'data/mail_template_data.xml',
        'views/hotel_reservation_view.xml',
        'views/reservation_pdf_print.xml',
        'views/registration_card.xml',
        'report/registration_card_template.xml',
        'report/reservation_confirm_template.xml',
        'report/report.xml'
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
