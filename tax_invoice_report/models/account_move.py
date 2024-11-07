from odoo import api, fields, models, tools, _


class AccMove(models.Model):
    _inherit = "account.move"

    def get_folio_data(self):
        for move in self:
            invoice_number = move.name
            if invoice_number:
                folio = self.env['hotel.folio'].search([('invoice_ids.name', '=', move.name)], limit=1)
                if folio and folio.room_lines:
                    room_line = folio.room_lines[0]

                    # Fetching payment move data, assuming the first one is sufficient
                    payment_move = folio.payment_move_ids and folio.payment_move_ids[0] or False
                    room_charge = room_line.product_id.room_charge or 0.0
                    meal_charge = room_line.product_id.meal_charge or 0.0
                    room_charge_10_percent = room_charge * 0.1
                    meal_charge_10_percent = meal_charge * 0.1
                    muncipality_fee = room_charge_10_percent + meal_charge_10_percent
                    product_price_tariff = room_line.product_id.lst_price or 0.0
                    total_advance = folio.total_advance or 0.0
                    amount_total = (product_price_tariff+muncipality_fee)-total_advance
                    vat_muncipal_included_tariff = product_price_tariff+muncipality_fee

                    return {
                        'checkin_date': room_line.checkin_date.strftime('%m/%d/%Y') if room_line.checkin_date else '',
                        'checkout_date': room_line.checkout_date.strftime('%m/%d/%Y') if room_line.checkout_date else '',
                        'sales_person': folio.user_id.name if folio.user_id else '',
                        'room_number': room_line.product_id.name if room_line.product_id else '',
                        'room_type': room_line.categ_id.name if room_line.categ_id else '',
                        'product_price_tariff': room_line.product_id.lst_price if room_line.product_id.lst_price else '',
                        'muncipality_fee': muncipality_fee,
                        'amount_total':amount_total,
                        'reservation_no': folio.reservation_id.name if folio.reservation_id else '',
                        'adults': folio.reservation_id.adults if folio.reservation_id else 0,
                        'childs': folio.reservation_id.childs if folio.reservation_id else 0,
                        'total_advance': folio.total_advance or 0.0,
                        'advance_payment_date': payment_move.date.strftime('%m/%d/%Y') if payment_move and payment_move.date else '',
                        'advance_ref_no': payment_move.name if payment_move else '',
                        'vat_muncipal_included_tariff':vat_muncipal_included_tariff
                    }
        return {}


    def get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        folio_data = self.get_folio_data()  # Retrieve all folio data

        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': docs,
            'checkin_date': folio_data.get('checkin_date'),
            'checkout_date': folio_data.get('checkout_date'),
            'sales_person': folio_data.get('sales_person'),
            'room_number': folio_data.get('room_number'),
            # 'arrival_date': folio_data.get('arrival_date'),
            # 'departure_date': folio_data.get('departure_date'),
        }