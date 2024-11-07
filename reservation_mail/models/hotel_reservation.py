from odoo import models, fields, api

class HotelReservation(models.Model):

    _inherit = 'hotel.reservation'

    def action_send_mail(self):
        template = self.env.ref('reservation_mail.email_template_registration_confirmation')
        email_values = {
            'email_from': self.env.user.email,
            'email_to': self.partner_id.email,
        }
        template.send_mail(self.id, email_values=email_values, force_send=True)