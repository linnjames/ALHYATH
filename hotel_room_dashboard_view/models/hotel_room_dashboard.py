# -*- coding: utf-8 -*-
import pytz

from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
import time
from datetime import date
from datetime import datetime, timedelta
from dateutil.parser import *
import pytz
import math

utc_time = datetime.utcnow()
import logging

_logger = logging.getLogger(__name__)


class hotel_room_dashboard(models.Model):
    """ Class for showing Rooms Dashboard"""
    _name = 'hotel.room.dashboard'
    _description = 'Room Dashboard'

    name = fields.Char('Name')

    def open_dashboard(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/hotel_room_dashboard/web/',
            'target': 'self',
        }

    def get_company_id(self):
        return self._context.get('allowed_company_ids')


class hotel_reservation(models.Model):
    _inherit = 'hotel.reservation'

    """ Inherited to set default values in reservation form"""

    def action_folio_confirm(self):
        search_id = self.env['hotel.folio'].search([('reservation_id', '=', self.id)])
        if search_id and search_id.state == 'draft':
            search_id.action_confirm()
        return True

    @api.model
    def get_data(self, shop_id):
        print('==========', shop_id)
        if shop_id:
            today = datetime.today().date()
            # Get rooms booked today based on the check-in and check-out dates
            booked = self.env['hotel.room.booking.history'].search([
                ('check_in', '<=', today),
                ('check_out', '>=', today)
            ])
            print(booked, "oooooooooooooooooo")

            # Get all rooms associated with the given shop
            all_rooms = self.env['hotel.room'].search([('shop_id', '=', int(shop_id))])
            print(all_rooms, "qqqqqqqqqqqqq,,,,,,,,,,,,,,,,,,,,,,,,,")

            # Get housekeeping records for rooms that are dirty today
            housekeeping_records = self.env['hotel.housekeeping'].search([
                ('current_date', '=', today),
                ('state', '=', 'dirty')
            ])
            print(housekeeping_records, "wwwwwwwwwwwwwwwwwwwwwww")

            # Separate rooms under cleaning and maintenance
            room_cleaning = []
            room_maintenance = []
            for record in housekeeping_records:
                if record.quality == 'clean':
                    room_cleaning.append(record)  # Add record to room_cleaning list
                elif record.quality == 'maintenance':
                    room_maintenance.append(record)  # Add record to room_maintenance list

            # Initialize lists to track room statuses
            total = []
            check_in = []
            check_out = []

            # Loop through each room and check for availability
            for room in all_rooms:
                has_booking_today = False
                for booking in room.room_folio_ids:
                    # Loop through each room associated with the booking
                    for booked_room in booking.history_id:
                        # Check if check-in is happening today
                        if booking.check_in.date() == today:
                            check_in.append(booked_room.id)

                        # Check if check-out is happening today
                        if booking.check_out.date() == today:
                            check_out.append(booked_room.id)

                        # Check if the room is booked today
                        if booking.check_in.date() <= today <= booking.check_out.date():
                            has_booking_today = True
                            break
                    if has_booking_today:
                        break

                # Add room to total list if it's not booked today
                if not has_booking_today:
                    total.append(room.id)

            print(total, 'Rooms available today')
            print(check_in, 'Rooms checking in today')
            print(check_out, 'Rooms checking out today')
            print(len(room_cleaning), 'Rooms Under Cleaning')
            print(len(room_maintenance), 'Rooms under Maintenance')

            return {
                'check_in': len(check_in),
                'check_out': len(check_out),
                'total': len(total),
                'booked': len(booked),
                'room_cleaning': len(room_cleaning),
                'room_maintenance': len(room_maintenance),
            }
        else:
            return {
                'check_in': '',
                'check_out': '',
                'total': '',
                'booked': '',
                'room_cleaning': '',
                'room_maintenance': '',
            }


    # @api.model
    # def get_data(self, shop_id):
    #     print('==========', shop_id)
    #     if shop_id:
    #         today = datetime.today().date()
    #         # check_in = self.env['hotel.folio'].search([('state', '=', 'draft'), ('shop_id', '=', int(shop_id))])
    #         # check_out = self.env['hotel.folio'].search([('state', '=', 'check_out'), ('shop_id', '=', int(shop_id))])
    #         # total = self.env['hotel.folio'].search([('shop_id', '=', int(shop_id))])
    #         # booked = self.env['hotel.folio'].search([('state', '!=', 'check_out'), ('shop_id', '=', int(shop_id))])
    #         booked = self.env['hotel.room.booking.history'].search([('check_in', '<=', today),('check_out', '>=', today)])
    #         print(booked,"oooooooooooooooooo")
    #         all_rooms = self.env['hotel.room'].search([('shop_id', '=', int(shop_id))])
    #         print(all_rooms,"qqqqqqqqqqqqq")
    #         housekeeping_records = self.env['hotel.housekeeping'].search([('current_date', '=', today),('state', '=', 'dirty')])
    #         print(housekeeping_records,"wwwwwwwwwwwwwwwwwwwwwww")
    #         room_cleaning = []
    #         room_maintenance = []
    #
    #         for record in housekeeping_records:
    #             if record.quality == 'clean':
    #                 room_cleaning.append(record)  # Add record to room_cleaning list
    #             elif record.quality == 'maintenance':
    #                 room_maintenance.append(record)  # Add record to room_maintenance list
    #
    #         total = []
    #         check_in = []
    #         check_out = []
    #         # total_available_rooms = []
    #         for room in all_rooms:
    #             has_booking_today = False
    #             for booking in room.room_folio_ids:
    #                 # Check if check-in is happening today
    #                 if booking.check_in.date() == today:
    #                     check_in.append(room.id)
    #
    #                 # Check if check-out is happening today
    #                 if booking.check_out.date() == today:
    #                     check_out.append(room.id)
    #                 if booking.check_in.date() <= today <= booking.check_out.date():
    #                     has_booking_today = True
    #                     break
    #             if not has_booking_today:
    #                 total.append(room.id)
    #
    #         print(total, 'Rooms available today')
    #         print(check_in, 'Rooms checking in today')
    #         print(check_out, 'Rooms checking out today')
    #         print(len(room_cleaning), 'Rooms Under Cleaning')
    #         print(len(room_maintenance), 'Rooms under Maintenance')
    #
    #         return {
    #             'check_in': len(check_in),
    #             'check_out': len(check_out),
    #             'total': len(total),
    #             'booked': len(booked),
    #             'room_cleaning': len(room_cleaning),
    #             'room_maintenance': len(room_maintenance),
    #         }
    #     else:
    #         return {
    #             'check_in': '',
    #             'check_out': '',
    #             'total': '',
    #             'booked': '',
    #             'room_cleaning': '',
    #             'room_maintenance': '',
    #         }
    #
    def action_folio_checkout(self):
        search_id = self.env['hotel.folio'].search([('reservation_id', '=', self.id)])
        if search_id and search_id.state == 'sale':
            search_id.action_checkout()

    def action_folio_done(self):
        search_id = self.env['hotel.folio'].search([('reservation_id', '=', self.id)])
        if search_id and search_id.state == 'check_out':
            search_id.action_done()

    def write(self, vals):

        # print("ffffffffffffffffffffffffffff", vals)

        return super(hotel_reservation, self).write(vals)

    def get_folio_status(self):
        folio_record = self.env['hotel.folio'].search([('reservation_id', '=', self.id)])

        if folio_record:
            return (folio_record.state, folio_record.id)

        return False

    def get_view_folio(self):

        folio_view = self.env['ir.ui.view'].search(
            [('xml_id', '=', 'hotel.view_hotel_folio1_form'), ('model', '=', 'hotel.folio')], limit=1)

        return folio_view.id

    # def update_reservation_old(self, resourceId, description):
    #     print("fffffffffffffffff", resourceId, description)

    def update_reservation_line(self, description, start, end, resourceId, start_only_date, end_only_date):
        _logger.info("UPDATE RESERVATION LINE===>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        reservation = self.env['hotel.reservation'].search([('reservation_no', '=', description)])

        if resourceId:
            room_id = self.env['product.product'].search([('id', '=', resourceId)])

        for line_id in reservation:
            for line in line_id.reservation_line:
                # Check if room_id exists within the many2many room_number field
                if room_id.id in line.room_number.ids:
                    if start:
                        line.write({'checkin': start})
                    if end:
                        line.write({'checkout': end})

                if reservation.state == 'confirm':
                    hotel_history = self.env['hotel.room.booking.history'].search([('booking_id', '=', reservation.id)])

                    for hotel_history_line in hotel_history:
                        # Check if room_id exists within the many2many room_number field
                        if room_id.id in line.room_number.ids and hotel_history.booking_id.id == line.line_id.id:
                            if hotel_history_line.name in line.room_number.mapped('name'):
                                if start:
                                    hotel_history_line.write({"check_in": start})
                                    hotel_history_line.write({"check_in_date": start_only_date})
                                if end:
                                    hotel_history_line.write({"check_out": end})
                                    hotel_history_line.write({"check_out_date": end_only_date})

        if reservation:
            folio = self.env['hotel.folio'].search([('reservation_id', '=', reservation.reservation_no)])

            for folio_line in folio.room_lines:
                if room_id.id in folio_line.product_id.ids:
                    if start:
                        folio_line.write({'checkin_date': start})
                    if end:
                        folio_line.write({'checkout_date': end})
                    folio_line.on_change_checkout()

    # def update_reservation_line(self, description, start, end, resourceId, start_only_date, end_only_date):
    #     # print("resourceId::::::::::::", description, resourceId, start1, end1, old_id, start_only_date, end_only_date)
    #     _logger.info("UPDATE RESERVATION LINE===>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #     reservation = self.env['hotel.reservation'].search([('reservation_no', '=', description)])
    #
    #     # print("reservation::::::::::::::::", reservation, resourceId)
    #
    #     if resourceId:
    #         room_id = self.env['product.product'].search([('id', '=', resourceId)])
    #         # print("room_id:::::::::", room_id)
    #     for line_id in reservation:
    #         for line in line_id.reservation_line:
    #             if line.room_number.id == room_id.id:
    #
    #                 # print("line_id::::::::::::", line_id.folio_id)
    #                 if start:
    #                     line.write({'checkin': start})
    #                 if end:
    #                     line.write({'checkout': end})
    #
    #             if reservation.state == 'confirm':
    #                 # print("reservation:::::::::::::::::", reservation.state)
    #
    #                 hotel_history = self.env['hotel.room.booking.history'].search([('booking_id', '=', reservation.id)])
    #                 # print("hotel_history::::::::::::::::::", hotel_history)
    #                 for hotel_history_line in hotel_history:
    #                     # print("hotel_history_line.product_id.id::::::::;", hotel_history_line.product_id,
    #                     #       line.room_number.name)
    #                     if hotel_history_line.product_id == line.room_number.id and hotel_history.booking_id.id == line.line_id.id:
    #                         if hotel_history_line.name == line.room_number.name:
    #                             if start:
    #                                 hotel_history_line.write({"check_in": start})
    #                                 hotel_history_line.write({"check_in_date": start_only_date})
    #                             if end:
    #                                 hotel_history_line.write({"check_out": end})
    #                                 hotel_history_line.write({"check_out_date": end_only_date})
    #
    #     if reservation:
    #         folio = self.env['hotel.folio'].search([('reservation_id', '=', reservation.reservation_no)])
    #         # print("folio:::::::::::::", folio)
    #
    #         for folio_line in folio.room_lines:
    #             # print("folio_line::::::::::;", folio_line.product_id, room_id.id)
    #
    #             if folio_line.product_id.id == room_id.id:
    #                 if start:
    #                     folio_line.write({'checkin_date': start})
    #                 if end:
    #                     folio_line.write({'checkout_date': end})
    #                 folio_line.on_change_checkout()

    # def update_room(self, description, resourceId, start1, end1, old_id, start_only_date, end_only_date):
    #     # print("resourceId::::::::::::", description, resourceId, start1, end1, old_id, start_only_date, end_only_date)
    #     # print("ffffffffffffff",)
    #     _logger.info("UPDATE ROOM===>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #     if resourceId:
    #         room_id = self.env['product.product'].search([('id', '=', resourceId)])
    #         # print("room_id:::::::::", room_id)
    #     if old_id:
    #         room_id_old = self.env['product.product'].search([('id', '=', old_id)])
    #         # print("room_id:::::::::", room_id_old)
    #
    #     reservation = self.env['hotel.reservation'].search([('reservation_no', '=', description)])
    #
    #     # print("rreservation::::::::::::::::", reservation, resourceId)
    #
    #     if resourceId:
    #         room_id = self.env['product.product'].search([('id', '=', resourceId)])
    #         # print("room_id:::::::::", room_id)
    #     for line_id in reservation:
    #         for line in line_id.reservation_line:
    #
    #             if room_id_old:
    #                 if line.room_number.id == room_id_old.id:
    #
    #                     # print("line_id::::::::::::", line_id.folio_id)
    #                     if start1:
    #                         line.write({'checkin': start1})
    #                     if end1:
    #                         line.write({'checkout': end1})
    #
    #                     if room_id:
    #                         line.write({'room_number': room_id.id})
    #                         line.write({'categ_id': room_id.categ_id.id})
    #             if reservation.state != 'draft':
    #                 # print("reservation:::::::::::.::::::",reservation.state)
    #
    #                 hotel_history = self.env['hotel.room.booking.history'].search([('booking_id', '=', reservation.id)])
    #                 hotel_room = self.env['hotel.room'].search([('product_id', '=', room_id.id)])
    #                 # print("hotel_history::::::::::::::::::", hotel_history)
    #                 for hotel_history_line in hotel_history:
    #                     # print("hotel_history_line.product_id.id::::::::;",hotel_history_line.product_id,room_id_old.id)
    #                     if hotel_history_line.product_id == room_id_old.id and hotel_history.booking_id.id == line.line_id.id:
    #                         # print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    #                         if start1:
    #                             hotel_history_line.write({"check_in": start1})
    #                             hotel_history_line.write({"check_in_date": start_only_date})
    #                         if end1:
    #                             hotel_history_line.write({"check_out": end1})
    #                             hotel_history_line.write({"check_out_date": end_only_date})
    #                         if hotel_room:
    #                             hotel_history_line.write({"history_id": hotel_room.id})
    #                             hotel_history_line.write({"name": hotel_room.name})
    #                         if room_id:
    #                             hotel_history_line.write({"product_id": room_id.id})
    #                             hotel_history_line.write({"category_id": room_id.categ_id.id})
    #
    #     if reservation:
    #         folio = self.env['hotel.folio'].search([('reservation_id', '=', reservation.reservation_no)])
    #         # print("folio:::::::::::::", folio)
    #
    #         for line in folio.room_lines:
    #             # print("line:::::::::", line)
    #             if room_id_old:
    #                 if line.product_id.id == room_id_old.id:
    #                     # print("line:::::::::::::::::::::::", line)
    #
    #                     if room_id:
    #                         line.write({"product_id": room_id.id})
    #                         line.write({"name": room_id.name})
    #                         line.write({"categ_id": room_id.categ_id.id})
    #
    #                     if end1:
    #                         # print("ffffffffffffffffffffffff2", end1)
    #                         line.write({'checkout_date': end1})
    #
    #                     if start1:
    #                         # print("ffffffffffffffffffffffff", start1)
    #                         line.write({'checkin_date': start1})
    #
    #                     line.on_change_checkout()
    #
    #             else:
    #                 if room_id:
    #                     line.write({"product_id": room_id.id})
    #                     line.write({"name": room_id.name})
    #                     line.write({"categ_id": room_id.categ_id.id})
    #
    #                 if end1:
    #                     # print("ffffffffffffffffffffffff2", end1)
    #                     line.write({'checkout_date': end1})
    #
    #                 if start1:
    #                     # print("ffffffffffffffffffffffff", start1)
    #                     line.write({'checkin_date': start1})
    #                 line.on_change_checkout()

    def update_room(self, description, resourceId, start1, end1, old_id, start_only_date, end_only_date):
        _logger.info("UPDATE ROOM===>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        room_id = self.env['product.product'].search([('id', '=', resourceId)]) if resourceId else False
        room_id_old = self.env['product.product'].search([('id', '=', old_id)]) if old_id else False

        reservation = self.env['hotel.reservation'].search([('reservation_no', '=', description)])

        for line_id in reservation:
            for line in line_id.reservation_line:
                if room_id_old and room_id_old.id in line.room_number.ids:
                    # Update check-in and check-out dates
                    if start1:
                        line.write({'checkin': start1})
                    if end1:
                        line.write({'checkout': end1})

                    # Update room number and category if new room_id is provided
                    if room_id:
                        line.write({'room_number': [(4, room_id.id)]})  # Add room_id to the many2many field
                        line.write({'categ_id': room_id.categ_id.id})

                if reservation.state != 'draft':
                    hotel_history = self.env['hotel.room.booking.history'].search([('booking_id', '=', reservation.id)])
                    hotel_room = self.env['hotel.room'].search([('product_id', '=', room_id.id)]) if room_id else False

                    for hotel_history_line in hotel_history:
                        if room_id_old and room_id_old.id == hotel_history_line.product_id.id and hotel_history_line.booking_id.id == line.line_id.id:
                            if start1:
                                hotel_history_line.write({"check_in": start1})
                                hotel_history_line.write({"check_in_date": start_only_date})
                            if end1:
                                hotel_history_line.write({"check_out": end1})
                                hotel_history_line.write({"check_out_date": end_only_date})
                            if hotel_room:
                                hotel_history_line.write({"history_id": hotel_room.id})
                                hotel_history_line.write({"name": hotel_room.name})
                            if room_id:
                                hotel_history_line.write({"product_id": room_id.id})
                                hotel_history_line.write({"category_id": room_id.categ_id.id})

        if reservation:
            folio = self.env['hotel.folio'].search([('reservation_id', '=', reservation.reservation_no)])

            for line in folio.room_lines:
                if room_id_old and line.product_id.id == room_id_old.id:
                    # Update room information
                    if room_id:
                        line.write({"product_id": room_id.id})
                        line.write({"name": room_id.name})
                        line.write({"categ_id": room_id.categ_id.id})
                    if start1:
                        line.write({'checkin_date': start1})
                    if end1:
                        line.write({'checkout_date': end1})
                    line.on_change_checkout()

                elif room_id:
                    line.write({"product_id": room_id.id})
                    line.write({"name": room_id.name})
                    line.write({"categ_id": room_id.categ_id.id})
                    if start1:
                        line.write({'checkin_date': start1})
                    if end1:
                        line.write({'checkout_date': end1})
                    line.on_change_checkout()

    # def set_checkin_checkout(self, vals):
    #     _logger.info("CHECK IN CHECKOUT===>>>>>>>>>>{}".format(vals))
    #     if self.env.user:
    #         user_id = self.env.user
    #         tz = pytz.timezone(user_id.tz)
    #         time_difference = tz.utcoffset(utc_time).total_seconds()
    #         _logger.info("#################{}".format(self._context))
    #         if self._context.get('shop_id'):
    #             checkout_policy_id = self.env['checkout.configuration'].search(
    #                 [('shop_id', '=', self._context.get('shop_id'))])
    #             _logger.info("Checkout Policy===>>>{}".format(checkout_policy_id))
    #
    #             if checkout_policy_id.name == 'custom':
    #                 time = int(checkout_policy_id.time)
    #
    #                 checkin = vals.get('checkin')
    #                 check_in_from_string = fields.Datetime.from_string(vals.get('checkin'))
    #                 checkin = datetime(check_in_from_string.year, check_in_from_string.month, check_in_from_string.day)
    #                 checkin = checkin + timedelta(hours=int(time))
    #
    #                 checkout = vals.get('checkout')
    #                 checkout_from_string = fields.Datetime.from_string(vals.get('checkout'))
    #                 checkout = datetime(checkout_from_string.year, checkout_from_string.month, checkout_from_string.day)
    #                 checkout = checkout + timedelta(hours=int(time))
    #
    #                 checkout = checkout - timedelta(seconds=time_difference)
    #                 checkin = checkin - timedelta(seconds=time_difference)
    #
    #                 _logger.info("\n\n\n\n\nVALS=====>>>>>>>>>>>>>>>>>>{}".format(checkout))
    #                 vals.update({'checkout': checkout, 'checkin': checkin})
    #     return vals


class RrHousekeeping(models.Model):
    """ Class for showing housekeeping Maintanance Dashboard"""
    _inherit = 'rr.housekeeping'

    def maintance_housekiping(self):
        maintance_dict_list = []
        for rec in self.search([]):
            if rec.state == 'assign':
                maintance_dict = {}
                maintance_dict.update({
                    'id': rec.id,
                    'date': rec.date.date(),
                    'room_no': [1, rec.room_no.name],
                    'state': "assign"
                })
                maintance_dict_list.append(maintance_dict)
        return maintance_dict_list
