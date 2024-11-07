from odoo import models, fields, api


class NightAuditReport(models.TransientModel):
    _name = 'night.audit.report.wiz'
    _description = 'Night Audit Report'


    date = fields.Date(string="Date", required=True, default=fields.Datetime.today())

    def generate_xlsx_report(self):
        print("aaaaaaaaaaaaaaaaaaaa")
        date = self.date

        datas = {
            'date': date,
        }
        return self.env.ref('night_audit_report.night_audit_report_xlsx').report_action(self, data=datas)