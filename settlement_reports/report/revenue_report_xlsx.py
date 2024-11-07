from odoo import models
import datetime


class RevenueReportXlsx(models.AbstractModel):
    _name = 'report.settlement_reports.revenue_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, docids):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        tax_excluded = data.get('tax_excluded')
        folio_records = self.env['hotel.folio'].sudo().search([('state', '=', 'done')])

        format1 = workbook.add_format({'font_size': 14, 'align': 'center_across', 'bold': True, 'font_color': 'black'})
        format2 = workbook.add_format({'font_size': 12, 'align': 'center_across', 'bold': True, 'bg_color': '#C0C0C0'})
        format5 = workbook.add_format({'font_size': 10, 'align': 'left'})

        sheet = workbook.add_worksheet('Revenue Report')
        sheet.merge_range(0, 0, 0, 11, self.env.company.name, format1)

        sheet.set_column('A:A', 15)
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
        sheet.set_column('L:L', 35)

        row = 1
        col = 0

        sheet.write(row, col, 'Room', format2)
        col += 1
        sheet.write(row, col, 'RegNO', format2)
        col += 1
        sheet.write(row, col, 'Checkout', format2)
        col += 1
        sheet.write(row, col, 'Bill No', format2)
        col += 1
        sheet.write(row, col, 'Bill Date', format2)
        col += 1
        sheet.write(row, col, 'Payment', format2)
        col += 1
        sheet.write(row, col, 'Debit', format2)
        col += 1
        sheet.write(row, col, 'Credit', format2)
        col += 1
        sheet.write(row, col, 'Net', format2)
        col += 1
        sheet.write(row, col, 'User', format2)
        col += 1
        sheet.write(row, col, 'Time', format2)
        row += 1

        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'align': 'left', 'font_size': 10})
        for folio in folio_records:
            col = 0

            room_no = folio.rooms_ref
            reg_no = folio.reservation_id.name

            checkout_dates = folio.room_lines.mapped('checkout_date')
            if checkout_dates:
                checkout_date = checkout_dates[0].strftime('%Y-%m-%d') if checkout_dates[0] else ''
            else:
                checkout_date = ''

            bill_no = ', '.join(folio.invoice_ids.mapped('name')) if folio.invoice_ids else ''

            # Convert invoice dates to strings
            bill_dates = folio.invoice_ids.mapped('invoice_date')
            bill_date = ', '.join(date.strftime('%Y-%m-%d') for date in bill_dates if
                                  isinstance(date, (datetime.date, datetime.datetime))) if bill_dates else ''

            # Compute credit and debit totals
            debit = 0
            if tax_excluded:
                credit = sum(invoice.amount_untaxed for invoice in folio.invoice_ids)
            else:
                credit = sum(invoice.amount_total for invoice in folio.invoice_ids)
            net_amount = debit - credit
            user_name = folio.user_id.name
            time_created = folio.create_date

            payment_data = ""
            if folio.invoice_ids:
                journal_names = []  # List to store journal names
                for invoice in folio.invoice_ids:
                    payment_widget = invoice.invoice_payments_widget
                    if payment_widget and payment_widget.get('content'):
                        payment_lines = payment_widget['content']
                        for line in payment_lines:
                            journal_names.append(line['journal_name'])  # Append journal_name to list

                # Join journal names with commas and store in payment_data
                payment_data = ','.join(journal_names)

            # payment_data = ""
            # if folio.invoice_ids:
            #     for invoice in folio.invoice_ids:
            #         payment_widget = invoice.invoice_payments_widget
            #         if payment_widget and payment_widget.get('content'):
            #             payment_lines = payment_widget['content']
            #             for line in payment_lines:
            #                 payment_data += f"{line['journal_name']}"

            sheet.write(row, col, room_no, format5)
            col += 1
            sheet.write(row, col, reg_no, format5)
            col += 1
            sheet.write(row, col, checkout_date, date_format)
            col += 1
            sheet.write(row, col, bill_no, format5)
            col += 1
            sheet.write(row, col, bill_date, date_format)
            col += 1
            sheet.write(row, col, payment_data, format5)
            col += 1
            sheet.write(row, col, debit, format5)
            col += 1
            sheet.write(row, col, credit, format5)
            col += 1
            sheet.write(row, col, net_amount, format5)
            col += 1
            sheet.write(row, col, user_name, format5)
            col += 1
            sheet.write(row, col, time_created.strftime('%Y-%m-%d %H:%M:%S'), format5)

            row += 1
