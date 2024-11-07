# -*- encoding: utf-8 -*-

{
    "name": "Custome Hotel Management",
    "version": "16.0.0.1.24",
    "category": "Generic Modules/Hotel Management",
    "description": """
    Hotel management module with extra features
    """,
    "depends": ["base", "account", 'stock', 'hotel_restaurant', 'hotel_housekeeping', 'sale_enhancement', 'product', 'hotel','hotel_management'],
    "init_xml": [],
    "demo_xml": [
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hotel_management_view.xml",
        "views/hotel_folio.xml",
        "views/product_product.xml",
        "views/hotel_room.xml",
    ],
    'images': ['static/description/icon.png'],
    "active": False,
    "installable": True,
    'license': 'OPL-1',
}
