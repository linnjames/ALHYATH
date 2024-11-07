from odoo import models, fields, api

class hotel_reservation_line(models.Model):
    _inherit = 'hotel.reservation.line'

    extra_bed = fields.Boolean(string="Extra Bed")
    early_checkin = fields.Datetime('Early Checkin')
    late_checkout = fields.Datetime('Late Checkout')
    tip = fields.Integer('Tip')

    @api.onchange('room_number')
    def room_tariff_calculation(self):
        for rec in self:
            total_price = 0
            if rec.room_number:
                for room in rec.room_number:
                    if rec.line_id.meal_id:
                        total_price += room.room_charge + room.meal_charge
                    else:
                        total_price += room.room_charge
                rec.price = total_price


class HotelReservation(models.Model):

    _inherit = 'hotel.reservation'

    def action_open_folios(self):
        folios = self.env['hotel.folio'].search([('reservation_id', '=', self.id)], limit=1)
        if folios:
            return {
                'name': 'Folio',
                'type': 'ir.actions.act_window',
                'res_model': 'hotel.folio',
                'view_mode': 'form',
                'res_id': folios.id,
            }
        else:
            return {'type': 'ir.actions.act_window_close'}


    def done(self):
        res = super(HotelReservation, self).done()
        for line in self.reservation_line:
            folio = self.env['hotel.folio'].search([('reservation_id', '=', self.id)])
            print(folio)

            if line.extra_bed:
                extra_bed_product = self.env['product.product'].search([('name', '=', 'Extra Bed')])
                if extra_bed_product:
                    vals = {
                        'folio_id': folio.id,
                        'product_id': extra_bed_product.id,
                        'name': extra_bed_product.name,
                    }
                    self.env["hotel_service.line"].create(vals)

            if line.early_checkin:
                early_checkin_product = self.env['product.product'].search([('name', '=', 'Early Checkin')])
                if early_checkin_product:
                    vals = {
                        'folio_id': folio.id,
                        'product_id': early_checkin_product.id,
                        'name': early_checkin_product.name,
                    }
                    self.env["hotel_service.line"].create(vals)
        return res





