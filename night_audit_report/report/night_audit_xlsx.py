from odoo import models
from datetime import datetime, timedelta

class NightAuditXlsx(models.AbstractModel):
    _name = 'report.night_audit_report.night_audit_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, docids):
        date_str = data.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())

        # Start and end of the month for MONTH's report
        start_of_month = date.replace(day=1)  # First day of the month
        next_month = (start_of_month + timedelta(days=32)).replace(day=1)  # First day of next month
        end_of_month = next_month - timedelta(days=1)  # Last day of the current month

        # Start and end of the year for YEAR's report
        start_of_year = date.replace(month=1, day=1)  # First day of the year
        next_year = (start_of_year + timedelta(days=366)).replace(day=1, month=1)  # First day of next year
        end_of_year = next_year - timedelta(days=1)  # Last day of the current year

        folio_records = self.env['hotel.folio'].sudo().search([
            ('state', '=', 'done'),
            ('create_date', '>=', start_of_day),
            ('create_date', '<=', end_of_day)
        ])

        # Fetch folio records for the MONTH
        folio_month_records = self.env['hotel.folio'].sudo().search([
            ('state', '=', 'done'),
            ('create_date', '>=', start_of_month),
            ('create_date', '<=', end_of_month)
        ])

        # Fetch folio records for the YEAR
        folio_year_records = self.env['hotel.folio'].sudo().search([
            ('state', '=', 'done'),
            ('create_date', '>=', start_of_year),
            ('create_date', '<=', end_of_year)
        ])
        print(folio_records)
        print(folio_month_records,"rrrrrrrrrrrrrrrrrrrrr")
        print(folio_year_records,"lllllllllllllllllllll")

        format1 = workbook.add_format({'font_size': 14, 'align': 'center_across', 'bold': True, 'font_color': 'black'})
        format2 = workbook.add_format({'font_size': 12, 'align': 'center_across', 'bold': True, 'bg_color': '#C0C0C0'})
        format3 = workbook.add_format({'font_size': 12, 'align': 'right', 'bold': True, 'bg_color': '#C0C0C0'})
        format5 = workbook.add_format({'font_size': 10, 'align': 'left'})
        format_amount = workbook.add_format({'font_size': 10, 'align': 'right', 'num_format': '#,##0.00'})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'align': 'left', 'font_size': 10})

        sheet = workbook.add_worksheet('Night Audit Report')
        sheet.merge_range(0, 0, 0, 14, self.env.company.name, format1)

        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 15)
        sheet.set_column('I:I', 15)
        sheet.set_column('J:J', 15)
        sheet.set_column('K:K', 15)
        sheet.set_column('L:L', 15)
        sheet.set_column('M:M', 15)
        sheet.set_column('N:N', 15)

        row = 1
        col = 0

        sheet.merge_range(row, col + 1, row, col + 3, 'Today', format2)  # Merge for Today
        sheet.merge_range(row, col + 4, row, col + 6, 'Month', format2)  # Merge for Month
        sheet.merge_range(row, col + 7, row, col + 9, 'Year', format2)  # Merge for Year

        row += 1

        # Headers for Amount, Allowance, and Net

        sheet.write(row, col, '', format2)
        sheet.write(row, col + 1, 'Amount', format2)
        sheet.write(row, col + 2, 'Allowance', format2)
        sheet.write(row, col + 3, 'Net', format2)

        # Write 'Amount', 'Allowance', and 'Net' headers under 'Month'
        sheet.write(row, col + 4, 'Amount', format2)
        sheet.write(row, col + 5, 'Allowance', format2)
        sheet.write(row, col + 6, 'Net', format2)

        # Write 'Amount', 'Allowance', and 'Net' headers under 'Year'
        sheet.write(row, col + 7, 'Amount', format2)
        sheet.write(row, col + 8, 'Allowance', format2)
        sheet.write(row, col + 9, 'Net', format2)

        row += 1

        total_room_revenue = 0
        for folio in folio_records:
            for line in folio.room_lines:
                total_room_revenue += line.price_subtotal
                print(total_room_revenue,'oooooooooo')

        room_revenue_allowance = 0
        for folio in folio_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Allowance':
                    room_revenue_allowance += line.price_subtotal
                    print(room_revenue_allowance)

        net_room_revenue = total_room_revenue - room_revenue_allowance


        extra_bed_total = 0
        for folio in folio_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Extra Bed':
                    extra_bed_total += line.price_subtotal
                    print(extra_bed_total,"pppppppp")

        early_checkin_total = 0
        for folio in folio_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Early Checkin':
                    early_checkin_total += line.price_subtotal
                    print(extra_bed_total)

        late_checkout_total = 0
        for folio in folio_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Late Checkout':
                    late_checkout_total += line.price_subtotal
                    print(late_checkout_total)

        manual_room_charge_total = 0
        for folio in folio_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Manual Room Charges':
                    manual_room_charge_total += line.price_subtotal
                    print(manual_room_charge_total)

        service_charge_total = 0
        for folio in folio_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Service Charge':
                    service_charge_total += line.price_subtotal
                    print(service_charge_total)


        total_room_service_charge = 0
        for folio in folio_records:
            for line in folio.room_service_food_lines:
                total_room_service_charge += line.price_subtotal

        total_restaurant_charge = 0
        for folio in folio_records:
            for line in folio.food_lines:
                total_restaurant_charge += line.price_subtotal

            for pos_order in folio.pos_order_ids:
                if pos_order.session_id.config_id.name == 'Shop':
                    total_restaurant_charge += pos_order.amount_total

        total_coffe_shop_charge = 0
        for folio in folio_records:
            for line in folio.coffee_shop_food_lines:
                total_coffe_shop_charge += line.price_subtotal

            for pos_order in folio.pos_order_ids:
                if pos_order.session_id.config_id.name == 'Coffee Shop':
                    print("wwwwwwwwwwwwww")
                    total_coffe_shop_charge += pos_order.amount_total
                    print(total_coffe_shop_charge)

        total_minibar_charge = 0
        for folio in folio_records:
            for line in folio.banquet_lines:
                total_minibar_charge += line.price_subtotal

        total_banquet_charge = 0
        for folio in folio_records:
            for line in folio.banquet_lines:
                total_banquet_charge += line.price_subtotal

        total_plan_charge = 0
        for folio in folio_records:
            for line in folio.room_lines:
                total_plan_charge += line.product_id.meal_charge
                print(total_plan_charge)

        total_laundry_charge = 0
        for folio in folio_records:
            for line in folio.laundry_line_ids:
                total_laundry_charge += line.price_subtotal
                print(total_laundry_charge)

        total_transport_charge = 0
        for folio in folio_records:
            for line in folio.transport_line_ids:
                total_transport_charge += line.price_subtotal
                print(total_transport_charge)

        total_telephone_charge = 0
        for folio in folio_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Telephone':
                    total_telephone_charge += line.price_subtotal

        total_miscellaneous_charge = 0
        for folio in folio_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Miscellaneous':
                    total_miscellaneous_charge += line.price_subtotal

        total_business_centre_charge = 0
        for folio in folio_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Business Centre':
                    total_business_centre_charge += line.price_subtotal

        total_roundoff = 0
        for folio in folio_records:
            for line in folio.invoice_ids:
                if line.invoice_cash_rounding_id:
                    account_id = line.invoice_cash_rounding_id.profit_account_id.id
                    move_lines = self.env['account.move.line'].search([
                        ('account_id', '=', account_id),
                        ('move_id.state', '=', 'posted')
                    ])
                    for move_line in move_lines:
                        total_roundoff += move_line.credit

        total_foreign_exchange_gain = 0
        for folio in folio_records:
            for line in folio.invoice_ids:
                # Access the payment widget (assuming it's already a dict)
                payment_widget = line.invoice_payments_widget
                if payment_widget:
                    # Iterate over payment entries in the widget
                    for payment in payment_widget.get('content', []):
                        # Check if the journal is 'Exchange Difference'
                        journal_name = payment.get('journal_name', '')
                        if journal_name == 'Exchange Difference':
                            print("yessssssssssssss")

                            # Get the journal entry ID (assuming it's in payment data)
                            journal_entry_id = payment.get('move_id', False)
                            print("ppppppppppp")

                            if journal_entry_id:
                                # Search for journal items (account.move.line) for this journal entry
                                journal_items = self.env['account.move.line'].search([
                                    ('move_id', '=', journal_entry_id),
                                    ('account_id.name', '=', 'Gain On Difference Of Exchange')
                                ])
                                print("ooooooooooooooo")

                                # Sum the credit amount for all matching journal items
                                for item in journal_items:
                                    total_foreign_exchange_gain += item.credit
                                    print(f"Total Foreign Exchange Gain (Year): {total_foreign_exchange_gain}")

        total_tax_amount = 0
        for folio in folio_records:
            for invoice in folio.invoice_ids:
                if invoice.amount_tax:
                    total_tax_amount += invoice.amount_tax
                    print(total_tax_amount)

        municipality_fee_total = 0
        for folio in folio_records:
            for line in folio.room_lines:
                meal_charge = line.product_id.meal_charge
                room_charge = line.product_id.room_charge
                municipality_fee_total += (0.10 * meal_charge) + (0.10 * room_charge)
                print(municipality_fee_total)


        #month
        total_room_revenue_month = 0
        for folio in folio_month_records:
            for line in folio.room_lines:
                total_room_revenue_month += line.price_subtotal

        room_revenue_allowance_month = 0
        for folio in folio_month_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Allowance':
                    room_revenue_allowance_month += line.price_subtotal
                    print(room_revenue_allowance_month)

        net_room_revenue_month = total_room_revenue_month - room_revenue_allowance_month


        extra_bed_total_month = 0
        for folio in folio_month_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Extra Bed':
                    extra_bed_total_month += line.price_subtotal

        early_checkin_total_month = 0
        for folio in folio_month_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Early Checkin':
                    early_checkin_total_month += line.price_subtotal

        late_checkout_total_month = 0
        for folio in folio_month_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Late Checkout':
                    late_checkout_total_month += line.price_subtotal

        manual_room_charge_total_month = 0
        for folio in folio_month_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Manual Room Charges':
                    manual_room_charge_total_month += line.price_subtotal
                    print(manual_room_charge_total_month)

        total_room_service_charge_month = 0
        for folio in folio_month_records:
            for line in folio.room_service_food_lines:
                total_room_service_charge_month += line.price_subtotal

        total_restaurant_charge_month = 0
        for folio in folio_month_records:
            for line in folio.food_lines:
                total_restaurant_charge_month += line.price_subtotal

            for pos_order in folio.pos_order_ids:
                if pos_order.session_id.config_id.name == 'Shop':
                    total_restaurant_charge += pos_order.amount_total

        total_coffe_shop_charge_month = 0
        for folio in folio_month_records:
            for line in folio.coffee_shop_food_lines:
                total_coffe_shop_charge_month += line.price_subtotal

            for pos_order in folio.pos_order_ids:
                if pos_order.session_id.config_id.name == 'Coffee Shop':
                    total_restaurant_charge += pos_order.amount_total

        total_minibar_charge_month = 0
        for folio in folio_month_records:
            for line in folio.banquet_lines:
                total_minibar_charge_month += line.price_subtotal

        total_banquet_charge_month = 0
        for folio in folio_month_records:
            for line in folio.banquet_lines:
                total_banquet_charge_month += line.price_subtotal

        total_plan_charge_month = 0
        for folio in folio_month_records:
            for line in folio.room_lines:
                total_plan_charge_month += line.product_id.meal_charge
                print(total_plan_charge_month)

        total_laundry_charge_month = 0
        for folio in folio_month_records:
            for line in folio.laundry_line_ids:
                total_laundry_charge_month += line.price_subtotal
                print(total_laundry_charge_month)

        total_transport_charge_month = 0
        for folio in folio_month_records:
            for line in folio.transport_line_ids:
                total_transport_charge_month += line.price_subtotal
                print(total_transport_charge_month)

        total_telephone_charge_month = 0
        for folio in folio_month_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Telephone':
                    total_telephone_charge_month += line.price_subtotal

        total_miscellaneous_charge_month = 0
        for folio in folio_month_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Miscellaneous':
                    total_miscellaneous_charge_month += line.price_subtotal

        total_business_centre_charge_month = 0
        for folio in folio_month_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Business Centre':
                    total_business_centre_charge_month += line.price_subtotal

        total_roundoff_month = 0
        for folio in folio_month_records:
            for line in folio.invoice_ids:
                if line.invoice_cash_rounding_id:
                    account_id = line.invoice_cash_rounding_id.profit_account_id.id
                    move_lines = self.env['account.move.line'].search([
                        ('account_id', '=', account_id),
                        ('move_id.state', '=', 'posted')
                    ])
                    for move_line in move_lines:
                        total_roundoff_month += move_line.credit

        total_foreign_exchange_gain_month = 0
        for folio in folio_month_records:
            for line in folio.invoice_ids:
                # Access the payment widget (assuming it's already a dict)
                payment_widget = line.invoice_payments_widget
                if payment_widget:
                    # Iterate over payment entries in the widget
                    for payment in payment_widget.get('content', []):
                        # Check if the journal is 'Exchange Difference'
                        journal_name = payment.get('journal_name', '')
                        if journal_name == 'Exchange Difference':
                            print("yessssssssssssss")

                            # Get the journal entry ID (assuming it's in payment data)
                            journal_entry_id = payment.get('move_id', False)
                            print("ppppppppppp")

                            if journal_entry_id:
                                # Search for journal items (account.move.line) for this journal entry
                                journal_items = self.env['account.move.line'].search([
                                    ('move_id', '=', journal_entry_id),
                                    ('account_id.name', '=', 'Gain On Difference Of Exchange')
                                ])
                                print("ooooooooooooooo")

                                # Sum the credit amount for all matching journal items
                                for item in journal_items:
                                    total_foreign_exchange_gain_month += item.credit
                                    print(f"Total Foreign Exchange Gain (Year): {total_foreign_exchange_gain_month}")

        total_tax_amount_month = 0
        for folio in folio_month_records:
            for invoice in folio.invoice_ids:
                if invoice.amount_tax:
                    total_tax_amount_month += invoice.amount_tax
                    print(total_tax_amount_month)

        service_charge_total_month = 0
        for folio in folio_month_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Service Charge':
                    service_charge_total_month += line.price_subtotal
                    print(service_charge_total_month)

        municipality_fee_total_month = 0
        for folio in folio_month_records:
            for line in folio.room_lines:
                meal_charge = line.product_id.meal_charge
                room_charge = line.product_id.room_charge
                municipality_fee_total_month += (0.10 * meal_charge) + (0.10 * room_charge)
                print(municipality_fee_total_month)

        # year
        total_room_revenue_year = 0
        for folio in folio_year_records:
            for line in folio.room_lines:
                total_room_revenue_year += line.price_subtotal

        room_revenue_allowance_year = 0
        for folio in folio_year_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Allowance':
                    room_revenue_allowance_year += line.price_subtotal
                    print(room_revenue_allowance_year)

        net_room_revenue_year = total_room_revenue_year - room_revenue_allowance_year

        extra_bed_total_year = 0
        for folio in folio_year_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Extra Bed':
                    extra_bed_total_year += line.price_subtotal

        early_checkin_total_year = 0
        for folio in folio_year_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Early Checkin':
                    early_checkin_total_year += line.price_subtotal

        late_checkout_total_year = 0
        for folio in folio_year_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Late Checkout':
                    late_checkout_total_year += line.price_subtotal

        manual_room_charge_total_year = 0
        for folio in folio_year_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Manual Room Charges':
                    manual_room_charge_total_year += line.price_subtotal
                    print(manual_room_charge_total_year)


        total_room_service_charge_year = 0
        for folio in folio_year_records:
            for line in folio.room_service_food_lines:
                total_room_service_charge_year += line.price_subtotal

        total_restaurant_charge_year = 0
        for folio in folio_year_records:
            for line in folio.food_lines:
                total_restaurant_charge_year += line.price_subtotal

            for pos_order in folio.pos_order_ids:
                if pos_order.session_id.config_id.name == 'Shop':
                    total_restaurant_charge += pos_order.amount_total

        total_coffe_shop_charge_year = 0
        for folio in folio_year_records:
            for line in folio.coffee_shop_food_lines:
                total_coffe_shop_charge_year += line.price_subtotal

            for pos_order in folio.pos_order_ids:
                if pos_order.session_id.config_id.name == 'Coffee Shop':
                    total_restaurant_charge += pos_order.amount_total

        total_minibar_charge_year = 0
        for folio in folio_year_records:
            for line in folio.banquet_lines:
                total_minibar_charge_year += line.price_subtotal

        total_banquet_charge_year = 0
        for folio in folio_year_records:
            for line in folio.banquet_lines:
                total_banquet_charge_year += line.price_subtotal

        total_plan_charge_year = 0
        for folio in folio_year_records:
            for line in folio.room_lines:
                total_plan_charge_year += line.product_id.meal_charge
                print(total_plan_charge_year)

        total_laundry_charge_year = 0
        for folio in folio_year_records:
            for line in folio.laundry_line_ids:
                total_laundry_charge_year += line.price_subtotal
                print(total_laundry_charge_year)

        total_transport_charge_year = 0
        for folio in folio_year_records:
            for line in folio.transport_line_ids:
                total_transport_charge_year += line.price_subtotal
                print(total_transport_charge)

        total_telephone_charge_year = 0
        for folio in folio_year_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Telephone':
                    total_telephone_charge_year += line.price_subtotal

        total_miscellaneous_charge_year = 0
        for folio in folio_year_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Miscellaneous':
                    total_miscellaneous_charge_year += line.price_subtotal

        total_business_centre_charge_year = 0
        for folio in folio_year_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Business Centre':
                    total_business_centre_charge_year += line.price_subtotal

        total_roundoff_year = 0
        for folio in folio_year_records:
            for line in folio.invoice_ids:
                if line.invoice_cash_rounding_id:
                    account_id = line.invoice_cash_rounding_id.profit_account_id.id
                    print(account_id,"ddddddddddddd")
                    move_lines = self.env['account.move.line'].search([
                        ('account_id', '=', account_id),
                        ('move_id.state', '=', 'posted')
                    ])
                    for move_line in move_lines:
                        total_roundoff_year += move_line.credit


        total_foreign_exchange_gain_year = 0
        for folio in folio_year_records:
            for line in folio.invoice_ids:
                # Access the payment widget (assuming it's already a dict)
                payment_widget = line.invoice_payments_widget
                if payment_widget:
                    # Iterate over payment entries in the widget
                    for payment in payment_widget.get('content', []):
                        # Check if the journal is 'Exchange Difference'
                        journal_name = payment.get('journal_name', '')
                        if journal_name == 'Exchange Difference':
                            print("yessssssssssssss")

                            # Get the journal entry ID (assuming it's in payment data)
                            journal_entry_id = payment.get('move_id', False)
                            print("ppppppppppp")

                            if journal_entry_id:
                                # Search for journal items (account.move.line) for this journal entry
                                journal_items = self.env['account.move.line'].search([
                                    ('move_id', '=', journal_entry_id),
                                    ('account_id.name', '=', 'Gain On Difference Of Exchange')
                                ])
                                print("ooooooooooooooo")

                                # Sum the credit amount for all matching journal items
                                for item in journal_items:
                                    total_foreign_exchange_gain_year += item.credit
                                    print(f"Total Foreign Exchange Gain (Year): {total_foreign_exchange_gain_year}")

        total_tax_amount_year = 0
        for folio in folio_year_records:
            for invoice in folio.invoice_ids:
                if invoice.amount_tax:
                    total_tax_amount_year += invoice.amount_tax
                    print(total_tax_amount_year)

        service_charge_total_year = 0
        for folio in folio_year_records:
            for line in folio.service_lines:
                if line.product_id.name == 'Service Charge':
                    service_charge_total_year += line.price_subtotal
                    print(service_charge_total_year)

        municipality_fee_total_year = 0
        for folio in folio_year_records:
            for line in folio.room_lines:
                meal_charge = line.product_id.meal_charge
                room_charge = line.product_id.room_charge
                municipality_fee_total_year += (0.10 * meal_charge) + (0.10 * room_charge)
                print(municipality_fee_total_year)

        revenue_breakdown_subtotal = (
                total_room_revenue +
                extra_bed_total +
                early_checkin_total +
                late_checkout_total +
                manual_room_charge_total
        )
        net_room_revenue_subtotal = revenue_breakdown_subtotal - room_revenue_allowance

        food_and_beverages_subtotal = (
                total_plan_charge +
                total_room_service_charge +
                total_restaurant_charge +
                total_coffe_shop_charge +
                total_banquet_charge
        )

        minor_operative_div_subtotal = (
                total_laundry_charge +
                total_transport_charge +
                total_telephone_charge +
                total_miscellaneous_charge +
                total_minibar_charge +
                total_business_centre_charge +
                total_foreign_exchange_gain +
                total_roundoff
        )

        taxes_subtotal = (
            total_tax_amount +
            service_charge_total +
            municipality_fee_total
        )

        total_revenue = (
            taxes_subtotal +
            minor_operative_div_subtotal +
            food_and_beverages_subtotal +
            revenue_breakdown_subtotal
        )
        total_day_net_revenue = total_revenue - room_revenue_allowance

        # month
        monthly_revenue_breakdown_subtotal = (
                total_room_revenue_month +
                extra_bed_total_month +
                early_checkin_total_month +
                late_checkout_total_month +
                manual_room_charge_total_month

        )
        monthly_net_room_revenue_subtotal = monthly_revenue_breakdown_subtotal - room_revenue_allowance_month

        monthly_food_and_beverages_subtotal = (
                total_plan_charge_month +
                total_room_service_charge_month +
                total_restaurant_charge_month +
                total_coffe_shop_charge_month +
                total_banquet_charge_month
        )
        monthly_minor_operative_div_subtotal = (
                total_laundry_charge_month +
                total_transport_charge_month +
                total_telephone_charge_month +
                total_miscellaneous_charge_month +
                total_minibar_charge_month +
                total_business_centre_charge_month +
                total_foreign_exchange_gain_month +
                total_roundoff_month

        )
        monthly_taxes_subtotal = (
                total_tax_amount_month +
                service_charge_total_month +
                municipality_fee_total_month
        )
        monthly_total_revenue = (
                monthly_taxes_subtotal +
                monthly_minor_operative_div_subtotal +
                monthly_food_and_beverages_subtotal +
                monthly_revenue_breakdown_subtotal
        )
        total_month_net_revenue = monthly_total_revenue - room_revenue_allowance_month

        # year
        yearly_revenue_breakdown_subtotal = (
                total_room_revenue_year +
                extra_bed_total_year +
                early_checkin_total_year +
                late_checkout_total_year +
                manual_room_charge_total
        )
        yearly_net_room_revenue_subtotal = yearly_revenue_breakdown_subtotal - room_revenue_allowance_year

        yearly_food_and_beverages_subtotal = (
                total_plan_charge_year +
                total_room_service_charge_year +
                total_restaurant_charge_year +
                total_coffe_shop_charge_year +
                total_banquet_charge_year
        )
        yearly_minor_operative_div_subtotal = (
                total_laundry_charge_year +
                total_transport_charge_year +
                total_telephone_charge_year +
                total_miscellaneous_charge_year +
                total_minibar_charge_year +
                total_business_centre_charge_year +
                total_foreign_exchange_gain_year +
                total_roundoff_year

        )
        yearly_taxes_subtotal = (
                total_tax_amount_year +
                service_charge_total_year +
                municipality_fee_total_year
        )
        yearly_total_revenue = (
                yearly_taxes_subtotal +
                yearly_minor_operative_div_subtotal +
                yearly_food_and_beverages_subtotal +
                yearly_revenue_breakdown_subtotal
        )
        total_yearly_net_revenue = yearly_total_revenue - room_revenue_allowance_year



        # Left section fields
        sheet.write(row, col, 'Revenue Breakdown', format2)  # Main heading
        row += 1
        sheet.write(row, col, 'Room Revenue', format5)
        sheet.write(row, col + 1, total_room_revenue, format_amount)
        # sheet.write(row, col + 2, room_revenue_allowance, format_amount)
        sheet.write(row, col + 3, net_room_revenue, format_amount)
        sheet.write(row, col + 4, total_room_revenue_month, format_amount)
        # sheet.write(row, col + 5, room_revenue_allowance_month, format_amount)
        sheet.write(row, col + 6, net_room_revenue_month, format_amount)
        sheet.write(row, col + 7, total_room_revenue_year, format_amount)
        # sheet.write(row, col + 8, room_revenue_allowance_year, format_amount)
        sheet.write(row, col + 9, net_room_revenue_year, format_amount)
        row += 1
        sheet.write(row, col, 'Extra Bed', format5)
        sheet.write(row, col + 1, extra_bed_total, format_amount)
        sheet.write(row, col + 3, extra_bed_total, format_amount)
        sheet.write(row, col + 4, extra_bed_total_month, format_amount)
        sheet.write(row, col + 6, extra_bed_total_month, format_amount)
        sheet.write(row, col + 7, extra_bed_total_year, format_amount)
        sheet.write(row, col + 9, extra_bed_total_year, format_amount)
        row += 1
        sheet.write(row, col, 'Early Checkin', format5)
        sheet.write(row, col + 1, early_checkin_total, format_amount)
        sheet.write(row, col + 3, early_checkin_total, format_amount)
        sheet.write(row, col + 4, early_checkin_total_month, format_amount)
        sheet.write(row, col + 6, early_checkin_total_month, format_amount)
        sheet.write(row, col + 7, early_checkin_total_year, format_amount)
        sheet.write(row, col + 9, early_checkin_total_year, format_amount)
        row += 1
        sheet.write(row, col, 'Late Checkout', format5)
        sheet.write(row, col + 1, late_checkout_total, format_amount)
        sheet.write(row, col + 3, late_checkout_total, format_amount)
        sheet.write(row, col + 4, late_checkout_total_month, format_amount)
        sheet.write(row, col + 6, late_checkout_total_month, format_amount)
        sheet.write(row, col + 7, late_checkout_total_year, format_amount)
        sheet.write(row, col + 9, late_checkout_total_year, format_amount)
        row += 1
        sheet.write(row, col, 'Manual Room Charges', format5)
        sheet.write(row, col + 1, manual_room_charge_total, format_amount)
        sheet.write(row, col + 3, manual_room_charge_total, format_amount)
        sheet.write(row, col + 4, manual_room_charge_total_month, format_amount)
        sheet.write(row, col + 6, manual_room_charge_total_month, format_amount)
        sheet.write(row, col + 7, manual_room_charge_total_year, format_amount)
        sheet.write(row, col + 9, manual_room_charge_total_year, format_amount)
        row += 1
        sheet.write(row, col, 'Subtotal', format3)
        sheet.write(row, col + 1, revenue_breakdown_subtotal, format_amount)
        sheet.write(row, col + 2, room_revenue_allowance, format_amount)
        sheet.write(row, col + 3, net_room_revenue_subtotal, format_amount)
        sheet.write(row, col + 4, monthly_revenue_breakdown_subtotal, format_amount)
        sheet.write(row, col + 5, room_revenue_allowance_month, format_amount)
        sheet.write(row, col + 6, monthly_net_room_revenue_subtotal, format_amount)
        sheet.write(row, col + 7, yearly_revenue_breakdown_subtotal, format_amount)
        sheet.write(row, col + 8, room_revenue_allowance_year, format_amount)
        sheet.write(row, col + 9, yearly_net_room_revenue_subtotal, format_amount)

        row += 2

        sheet.write(row, col, 'Food & Beverages', format2)
        row += 1
        sheet.write(row, col, 'Plan', format5)
        sheet.write(row, col + 1, total_plan_charge, format_amount)
        sheet.write(row, col + 3, total_plan_charge, format_amount)
        sheet.write(row, col + 4, total_plan_charge_month, format_amount)
        sheet.write(row, col + 6, total_plan_charge_month, format_amount)
        sheet.write(row, col + 7, total_plan_charge_year, format_amount)
        sheet.write(row, col + 9, total_plan_charge_year, format_amount)
        row += 1
        sheet.write(row, col, 'Room Service Food', format5)
        sheet.write(row, col + 1, total_room_service_charge, format_amount)
        sheet.write(row, col + 3, total_room_service_charge, format_amount)
        sheet.write(row, col + 4, total_room_service_charge_month, format_amount)
        sheet.write(row, col + 6, total_room_service_charge_month, format_amount)
        sheet.write(row, col + 7, total_room_service_charge_year, format_amount)
        sheet.write(row, col + 9, total_room_service_charge_year, format_amount)
        row += 1
        sheet.write(row, col, 'Restaurant Food', format5)
        sheet.write(row, col + 1, total_restaurant_charge, format_amount)
        sheet.write(row, col + 3, total_restaurant_charge, format_amount)
        sheet.write(row, col + 4, total_restaurant_charge_month, format_amount)
        sheet.write(row, col + 6, total_restaurant_charge_month, format_amount)
        sheet.write(row, col + 7, total_restaurant_charge_year, format_amount)
        sheet.write(row, col + 9, total_restaurant_charge_year, format_amount)
        row += 1
        sheet.write(row, col, 'Coffee Shop Food', format5)
        sheet.write(row, col + 1, total_coffe_shop_charge, format_amount)
        sheet.write(row, col + 3, total_coffe_shop_charge, format_amount)
        sheet.write(row, col + 4, total_coffe_shop_charge_month, format_amount)
        sheet.write(row, col + 6, total_coffe_shop_charge_month, format_amount)
        sheet.write(row, col + 7, total_coffe_shop_charge_year, format_amount)
        sheet.write(row, col + 9, total_coffe_shop_charge_year, format_amount)
        row += 1
        sheet.write(row, col, 'Banquet Food', format5)
        sheet.write(row, col + 1, total_banquet_charge, format_amount)
        sheet.write(row, col + 3, total_banquet_charge, format_amount)
        sheet.write(row, col + 4, total_banquet_charge_month, format_amount)
        sheet.write(row, col + 6, total_banquet_charge_month, format_amount)
        sheet.write(row, col + 7, total_banquet_charge_year, format_amount)
        sheet.write(row, col + 9, total_banquet_charge_year, format_amount)
        row += 1
        sheet.write(row, col, 'Subtotal', format3)
        sheet.write(row, col + 1, food_and_beverages_subtotal, format_amount)
        sheet.write(row, col + 3, food_and_beverages_subtotal, format_amount)
        sheet.write(row, col + 4, monthly_food_and_beverages_subtotal, format_amount)
        sheet.write(row, col + 6, monthly_food_and_beverages_subtotal, format_amount)
        sheet.write(row, col + 7, yearly_food_and_beverages_subtotal, format_amount)
        sheet.write(row, col + 9, yearly_food_and_beverages_subtotal, format_amount)


        row += 2

        sheet.write(row, col, 'Minor Operative Div', format2)
        row += 1
        sheet.write(row, col, 'Telephone', format5)
        sheet.write(row, col + 1, total_telephone_charge, format_amount)
        sheet.write(row, col + 3, total_telephone_charge, format_amount)
        sheet.write(row, col + 4, total_telephone_charge_month, format_amount)
        sheet.write(row, col + 6, total_telephone_charge_month, format_amount)
        sheet.write(row, col + 7, total_telephone_charge_month, format_amount)
        sheet.write(row, col + 9, total_telephone_charge_month, format_amount)
        row += 1
        sheet.write(row, col, 'Laundry', format5)
        sheet.write(row, col + 1, total_laundry_charge, format_amount)
        sheet.write(row, col + 3, total_laundry_charge, format_amount)
        sheet.write(row, col + 4, total_laundry_charge_month, format_amount)
        sheet.write(row, col + 6, total_laundry_charge_month, format_amount)
        sheet.write(row, col + 7, total_laundry_charge_year, format_amount)
        sheet.write(row, col + 9, total_laundry_charge_year, format_amount)
        row += 1
        sheet.write(row, col, 'Miscellaneous', format5)
        sheet.write(row, col + 1, total_miscellaneous_charge, format_amount)
        sheet.write(row, col + 3, total_miscellaneous_charge, format_amount)
        sheet.write(row, col + 4, total_miscellaneous_charge_month, format_amount)
        sheet.write(row, col + 6, total_miscellaneous_charge_month, format_amount)
        sheet.write(row, col + 7, total_miscellaneous_charge_year, format_amount)
        sheet.write(row, col + 9, total_miscellaneous_charge_year, format_amount)
        row += 1
        sheet.write(row, col, 'Round Off', format5)
        sheet.write(row, col + 1, total_roundoff, format_amount)
        sheet.write(row, col + 3, total_roundoff, format_amount)
        sheet.write(row, col + 4, total_roundoff_month, format_amount)
        sheet.write(row, col + 6, total_roundoff_month, format_amount)
        sheet.write(row, col + 7, total_roundoff_year, format_amount)
        sheet.write(row, col + 9, total_roundoff_year, format_amount)
        row += 1
        sheet.write(row, col, 'Minibar', format5)
        sheet.write(row, col + 1, total_minibar_charge, format_amount)
        sheet.write(row, col + 3, total_minibar_charge, format_amount)
        sheet.write(row, col + 4, total_minibar_charge_month, format_amount)
        sheet.write(row, col + 6, total_minibar_charge_month, format_amount)
        sheet.write(row, col + 7, total_minibar_charge_year, format_amount)
        sheet.write(row, col + 9, total_minibar_charge_year, format_amount)
        row += 1
        sheet.write(row, col, 'Business Centre', format5)
        sheet.write(row, col + 1, total_business_centre_charge, format_amount)
        sheet.write(row, col + 3, total_business_centre_charge, format_amount)
        sheet.write(row, col + 4, total_business_centre_charge_month, format_amount)
        sheet.write(row, col + 6, total_business_centre_charge_month, format_amount)
        sheet.write(row, col + 7, total_business_centre_charge_year, format_amount)
        sheet.write(row, col + 9, total_business_centre_charge_year, format_amount)
        row += 1
        sheet.write(row, col, 'Transport', format5)
        sheet.write(row, col + 1, total_transport_charge, format_amount)
        sheet.write(row, col + 3, total_transport_charge, format_amount)
        sheet.write(row, col + 4, total_transport_charge_month, format_amount)
        sheet.write(row, col + 6, total_transport_charge_month, format_amount)
        sheet.write(row, col + 7, total_transport_charge_year, format_amount)
        sheet.write(row, col + 9, total_transport_charge_year, format_amount)
        row += 1
        sheet.write(row, col, 'Foreign Exchange Gain', format5)
        sheet.write(row, col + 1, total_foreign_exchange_gain, format_amount)
        sheet.write(row, col + 3, total_foreign_exchange_gain, format_amount)
        sheet.write(row, col + 4, total_foreign_exchange_gain_month, format_amount)
        sheet.write(row, col + 6, total_foreign_exchange_gain_month, format_amount)
        sheet.write(row, col + 7, total_foreign_exchange_gain_year, format_amount)
        sheet.write(row, col + 9, total_foreign_exchange_gain_year, format_amount)
        row += 1
        sheet.write(row, col, 'Subtotal', format3)
        sheet.write(row, col + 1, minor_operative_div_subtotal, format_amount)
        sheet.write(row, col + 3, minor_operative_div_subtotal, format_amount)
        sheet.write(row, col + 4, monthly_minor_operative_div_subtotal, format_amount)
        sheet.write(row, col + 6, monthly_minor_operative_div_subtotal, format_amount)
        sheet.write(row, col + 7, yearly_minor_operative_div_subtotal, format_amount)
        sheet.write(row, col + 9, yearly_minor_operative_div_subtotal, format_amount)

        row += 2

        sheet.write(row, col, 'Taxes', format2)
        row += 1
        sheet.write(row, col, 'Vat 5%', format5)
        sheet.write(row, col + 1, total_tax_amount, format_amount)
        sheet.write(row, col + 3, total_tax_amount, format_amount)
        sheet.write(row, col + 4, total_tax_amount_month, format_amount)
        sheet.write(row, col + 6, total_tax_amount_month, format_amount)
        sheet.write(row, col + 7, total_tax_amount_year, format_amount)
        sheet.write(row, col + 9, total_tax_amount_year, format_amount)
        row += 1
        sheet.write(row, col, 'Municipality Fee', format5)
        sheet.write(row, col + 1, municipality_fee_total, format_amount)
        sheet.write(row, col + 3, municipality_fee_total, format_amount)
        sheet.write(row, col + 4, municipality_fee_total_month, format_amount)
        sheet.write(row, col + 6, municipality_fee_total_month, format_amount)
        sheet.write(row, col + 7, municipality_fee_total_year, format_amount)
        sheet.write(row, col + 9, municipality_fee_total_year, format_amount)
        row += 1
        sheet.write(row, col, 'Service Charge', format5)
        sheet.write(row, col + 1, service_charge_total, format_amount)
        sheet.write(row, col + 3, service_charge_total, format_amount)
        sheet.write(row, col + 4, service_charge_total_month, format_amount)
        sheet.write(row, col + 6, service_charge_total_month, format_amount)
        sheet.write(row, col + 7, service_charge_total_year, format_amount)
        sheet.write(row, col + 9, service_charge_total_year, format_amount)

        row += 1
        sheet.write(row, col, 'Subtotal', format3)
        sheet.write(row, col + 1, taxes_subtotal, format_amount)
        sheet.write(row, col + 3, taxes_subtotal, format_amount)
        sheet.write(row, col + 4, monthly_taxes_subtotal, format_amount)
        sheet.write(row, col + 6, monthly_taxes_subtotal, format_amount)
        sheet.write(row, col + 7, yearly_taxes_subtotal, format_amount)
        sheet.write(row, col + 9, yearly_taxes_subtotal, format_amount)
        row += 1
        sheet.write(row, col, 'Total Revenue', format3)
        sheet.write(row, col + 1, total_revenue, format_amount)
        sheet.write(row, col + 3, total_day_net_revenue, format_amount)
        sheet.write(row, col + 4, monthly_total_revenue, format_amount)
        sheet.write(row, col + 6, total_month_net_revenue, format_amount)
        sheet.write(row, col + 7, yearly_total_revenue, format_amount)
        sheet.write(row, col + 9, total_yearly_net_revenue, format_amount)

