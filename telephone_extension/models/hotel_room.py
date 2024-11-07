from odoo import models, fields, api
from datetime import datetime


class HotelRoom(models.Model):
    _inherit = 'hotel.room'

    telephone_extension = fields.Char(string="Phone Extension")

    @api.onchange('telephone_extension')
    def get_full_phone(self):
        for partner in self:
            full_phone = self.company_id.phone
            if self.phone_extension:
                full_phone += f" ext. {full_phone.phone_extension}"
                print(full_phone)
            return full_phone
