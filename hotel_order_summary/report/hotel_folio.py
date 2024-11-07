from odoo import models, fields, api

class HotelFolio(models.Model):
    _inherit = 'hotel.folio'

    def action_print_order_summary(self):
        return self.env.ref('hotel_order_summary.hotel_folio_order_summary').report_action(self)
