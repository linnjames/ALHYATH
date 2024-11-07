# -*- coding: utf-8 -*-
{
	'name': 'Telephone Extension',
	'version': '16.0.1.0.0',
	'summary': 'Telephone Extension',
	'description': 'Telephone Extension',
	 "depends": ["base", "account", 'stock', 'hotel_restaurant', 'hotel_housekeeping', 'sale_enhancement', 'product', 'hotel','hotel_management'],
	'data': [
		'views/hotel_room.xml'
	],
	'images': ['static/description/banner.png'],
	'license': 'AGPL-3',
	'installable': True,
	'auto_install': False,
	'application': False,
}
