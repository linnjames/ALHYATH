# -*- encoding: utf-8 -*-
{
    "name": "POS Restaurant Invoice",
    "version": "16.0.0.1.24",
    "author": "Febno",
    "category": "Generic Modules/Hotel Management",
    "description": """
    Restaurant handling by pos in hotel management
    """,
    "depends": ['point_of_sale', 'hotel_management', 'hotel_restaurant', 'hotel', "sale_enhancement"],
    "data": [
        'views/pos_config_views.xml'
    ],
    'assets': {
            'point_of_sale.assets': [
                'pos_restaurant_invoice/static/src/js/invoice_pos.js',
                'pos_restaurant_invoice/static/src/js/invoice_pdf.js',
            ],
    },
    'images': ['static/description/icon.png'],
    "active": False,
    "installable": True,
    'license': 'OPL-1',
}
