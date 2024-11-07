from odoo import models, fields, api


class RevenueReport(models.TransientModel):
    _name = 'revenue.report.wiz'
    _description = 'Revenue Wise Settlement Report'


    start_date = fields.Date(string="Start Date", required=True, default=fields.Datetime.today())
    end_date = fields.Date(string="End Date", required=True, default=fields.Datetime.today())
    tax_excluded = fields.Boolean("Tax Excluded")

    def generate_xlsx_report(self):
        print("aaaaaaaaaaaaaaaaaaaa")
        start_date = self.start_date
        end_date = self.end_date
        tax_excluded = self.tax_excluded

        datas = {
            'start_date': start_date,
            'end_date': end_date,
            'tax_excluded': tax_excluded,
        }
        return self.env.ref('settlement_reports.revenue_report_excel_xlsx').report_action(self, data=datas)
