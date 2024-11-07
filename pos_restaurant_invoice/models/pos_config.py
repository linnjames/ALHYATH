# -*- coding: utf-8 -*-
from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_auto_invoice = fields.Boolean(
        string="Enable Auto Invoice",
        config_parameter='pos_restaurant_invoice.enable_auto_invoice'
    )

    automatic_invoice_printing = fields.Boolean(
        string="Automatic Invoice Printing",
        config_parameter='pos_restaurant_invoice.automatic_invoice_printing'
    )
