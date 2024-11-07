from odoo import api, fields, models, tools, _


class ResCompany(models.Model):
    _inherit = "res.company"

    company_arabic = fields.Char(string="Arabic Name")
