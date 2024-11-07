from odoo import models, fields, api


class DayReport(models.TransientModel):
    _name = 'day.report.wiz'
    _description = 'Day wise Settlement Report'


    date = fields.Date(string="Date", required=True, default=fields.Datetime.today())

    def generate_xlsx_report(self):
        print("aaaaaaaaaaaaaaaaaaaa")
        date = self.date

        datas = {
            'date': date,
        }
        return self.env.ref('settlement_reports.day_report_excel_xlsx').report_action(self, data=datas)