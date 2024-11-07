from odoo import models, fields, api
from datetime import datetime


class HotelRoom(models.Model):
    _inherit = 'hotel.room'

    product_id = fields.Many2one('product.product', string='Product')

    status = fields.Selection(
        [
         ('vacant', 'Vacant'),
         ('booking', 'Booking'),
         ('occupied', 'Occupied'),
         ('clean', 'Cleaning'),
         ('maintenance', 'Maintenance')],
        default='available',
        string='Status', compute='compute_room_status'
    )

    def compute_room_status(self):
        today = datetime.today().date()
        for record in self:
            print(record.name)
            draft_reserve = self.env['hotel.reservation.line'].sudo().search([
                ('checkin', '<=', today),
                ('checkout', '>=', today),
                ('room_number', '=', record.product_id.id), ('line_id.state', '=', 'draft')
            ])
            bookings = self.env['hotel.room.booking.history'].sudo().search([
                ('check_in', '<=', today),
                ('check_out', '>=', today),
                ('history_id.name', '=', record.name)
            ])
            room_housekeeping = self.env['hotel.housekeeping'].sudo().search([
                ('current_date', '=', today),
                ('state', 'in', ['dirty', 'clean', 'inspect']),
                ('room_no', '=', record.product_id.id)
            ])
            if bookings:
                record.status = 'occupied'
            elif draft_reserve:
                record.status = 'booking'
            elif room_housekeeping:
                if room_housekeeping.quality == 'clean':
                    record.status = 'clean'
                elif room_housekeeping.quality == 'maintenance':
                    record.status = 'maintenance'
            else:
                record.status = 'vacant'

class HotelRoomBookingHistory(models.Model):
    _inherit = 'hotel.room.booking.history'

    @api.model
    def create(self, vals):
        record = super(HotelRoomBookingHistory, self).create(vals)
        if record.history_id:
            record.history_id.compute_room_status()
        return record

    def write(self, vals):
        result = super(HotelRoomBookingHistory, self).write(vals)
        if self.history_id:
            self.history_id.compute_room_status()
        return result



