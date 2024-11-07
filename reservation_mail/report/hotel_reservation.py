from odoo import models, fields, api
from datetime import datetime

class HotelReservation(models.Model):

    _inherit = 'hotel.reservation'

    def action_print_reservation_pdf(self):
        return self.env.ref('reservation_mail.hotel_reservation_confirmation_report').report_action(self)

    def action_print_registration_card(self):
        return self.env.ref('reservation_mail.hotel_registration_card').report_action(self)
