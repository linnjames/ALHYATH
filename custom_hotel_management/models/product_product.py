
from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_meal_product = fields.Boolean(string="Meal Include")
    meal_charge = fields.Float(string="Meal Charge", required=True)
    is_room = fields.Boolean(string="Room Tariff")
    room_charge = fields.Float(atring="Room Charge")

    @api.onchange('is_meal_product')
    def _onchange_is_meal_product(self):
        if not self.is_meal_product:
            self.meal_charge = 0

    @api.onchange('is_room')
    def _onchange_is_room(self):
        if not self.is_room:
            self.room_charge = 0

    @api.onchange('meal_charge', 'room_charge')
    def onchange_tariff(self):
        if self.meal_charge and self.room_charge:
            self.lst_price = self.meal_charge + self.room_charge

