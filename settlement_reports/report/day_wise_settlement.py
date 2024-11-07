from odoo import models
from datetime import datetime, timedelta

class DayReportXlsx(models.AbstractModel):
    _name = 'report.settlement_reports.day_report_excel_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, docids):
        date_str = data.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())

        folio_records = self.env['hotel.folio'].sudo().search([
            ('state', '=', 'done'),
            ('create_date', '>=', start_of_day),
            ('create_date', '<=', end_of_day)
        ])

        print(folio_records)

        format1 = workbook.add_format({'font_size': 14, 'align': 'center_across', 'bold': True, 'font_color': 'black'})
        format2 = workbook.add_format({'font_size': 12, 'align': 'center_across', 'bold': True, 'bg_color': '#C0C0C0'})
        format5 = workbook.add_format({'font_size': 10, 'align': 'left'})

        sheet = workbook.add_worksheet('Day wise Report')
        sheet.merge_range(0, 0, 0, 11, self.env.company.name, format1)

        sheet.set_column('A:A', 15)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 30)
        sheet.set_column('I:I', 15)
        sheet.set_column('J:J', 15)
        sheet.set_column('K:K', 15)
        sheet.set_column('L:L', 35)
        sheet.set_column('M:M', 35)

        row = 1
        col = 0

        sheet.write(row, col, 'Bill No', format2)
        col += 1
        sheet.write(row, col, 'Room No', format2)
        col += 1
        sheet.write(row, col, 'Reg No', format2)
        col += 1
        sheet.write(row, col, 'Guest Name', format2)
        col += 1
        sheet.write(row, col, 'Total Amount', format2)
        col += 1
        sheet.write(row, col, 'Cash', format2)
        col += 1
        sheet.write(row, col, 'CR Card', format2)
        col += 1
        sheet.write(row, col, 'Company', format2)
        col += 1
        sheet.write(row, col, 'Tip', format2)
        col += 1
        sheet.write(row, col, 'Created By', format2)
        col += 1
        sheet.write(row, col, 'Created Time', format2)
        col += 1
        sheet.write(row, col, 'Amend By', format2)
        col += 1
        sheet.write(row, col, 'Remark', format2)
        row += 1

        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'align': 'left','font_size': 10})

        for folio in folio_records:
            col = 0

            room_no = folio.rooms_ref
            reg_no = folio.reservation_id.name
            guest = folio.partner_id.name
            bill_no = folio.invoice_ids.name
            total = folio.invoice_ids.amount_total
            cash = 0
            card = 0
            company = folio.company_id.name
            created_by = folio.create_uid.name
            amend_by = folio.create_uid.name
            time_created = folio.create_date
            tip_list = [str(room_line.tip) for room_line in folio.room_lines if room_line.tip]
            tip = ','.join(tip_list) if tip_list else '0'

            remarks = []
            for invoice in folio.invoice_ids:
                payments = self.env['account.payment'].search([('ref', '=', invoice.name)])
                # payments = self.env['account.payment'].search([('id', '=', invoice.payment_ids.id)])
                print(payments)
                print(invoice)
                for payment in payments:
                    if payment.ref:
                        remarks.append(payment.ref)

            remark = ', '.join(remarks)

            if folio.invoice_ids:
                for invoice in folio.invoice_ids:
                    payment_widget = invoice.invoice_payments_widget
                    if payment_widget and payment_widget.get('content'):
                        payment_lines = payment_widget['content']
                        for line in payment_lines:
                            if line['journal_name'].lower() == 'cash':
                                cash += line['amount']
                            else:
                                card += line['amount']

            sheet.write(row, col, bill_no, format5)
            col += 1
            sheet.write(row, col, room_no, format5)
            col += 1
            sheet.write(row, col, reg_no, date_format)
            col += 1
            sheet.write(row, col, guest, format5)
            col += 1
            sheet.write(row, col, total, format5)
            col += 1
            sheet.write(row, col, cash, format5)
            col += 1
            sheet.write(row, col, card, format5)
            col += 1
            sheet.write(row, col, company, format5)
            col += 1
            sheet.write(row, col, tip, format5)
            col += 1
            sheet.write(row, col, created_by, format5)
            col += 1
            sheet.write(row, col, time_created.strftime('%Y-%m-%d %H:%M:%S'), format5)
            col += 1
            sheet.write(row, col, amend_by, format5)
            col += 1
            sheet.write(row, col, remark, format5)
            row += 1