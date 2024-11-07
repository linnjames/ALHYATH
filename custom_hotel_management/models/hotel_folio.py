from odoo import models, fields, api

class hotel_folio_line(models.Model):
    _inherit = 'hotel_folio.line'

    late_checkout = fields.Datetime('Late Checkout')
    late_checkout_charge = fields.Float("Late Checkout Charge")
    tip = fields.Integer('Tip')

    @api.onchange('late_checkout')
    def create_late_checkout(self):
        for record in self:
            if record.late_checkout:
                folio = self.env['hotel.folio'].search([('reservation_id', '=', self.folio_id.reservation_id.id)])
                print(folio)
                product_id = self.env['product.product'].search([('name', '=', 'Late Checkout')])
                print(product_id)
                if product_id:
                    vals = {
                        'folio_id': folio.id,
                        'product_id': product_id.id,
                        'name': product_id.name,
                    }
                    self.env["hotel_service.line"].create(vals)


class hotel_folio(models.Model):
    _inherit = 'hotel.folio'

    room_service_food_lines = fields.One2many('room_food.line', 'folio_id')
    coffee_shop_food_lines = fields.One2many('coffee_shop_food.line', 'folio_id')
    minibar_lines = fields.One2many('minibar.line', 'folio_id')
    banquet_lines = fields.One2many('banquet.line', 'folio_id')


class RoomFoodLine(models.Model):
    _name = 'room_food.line'
    _description = 'Room Food Service line'
    _inherits = {'sale.order.line': 'room_food_line_id'}

    room_food_line_id = fields.Many2one('sale.order.line', 'room_food_line_id', required=True, ondelete='cascade')
    folio_id = fields.Many2one('hotel.folio', 'Folio', ondelete='cascade')
    source_origin = fields.Char('Source Origin')
    product_uom_qty = fields.Float(string='Quantity', default=0.0)

    @api.model_create_multi
    def create(self, vals_list):
        for rec in vals_list:
            folio = self.env["hotel.folio"].browse(rec['folio_id'])
            if folio:
                rec.update({'order_id': folio.order_id.id})
        res = super(RoomFoodLine, self).create(vals_list)

        for line in res:
            if not line.price_unit and line.product_id:
                line.price_unit = line.product_id.lst_price
        return res

    @api.onchange('product_id')
    def product_id_change(self):
        self.ensure_one()

        if self.product_id:
            self.product_uom = self.product_id.uom_id
            self.price_unit = self.product_id.lst_price
            self.name = self.product_id.description_sale or self.product_id.name


            if not self.order_id:
                if self.folio_id:
                    self.order_id = self.folio_id.order_id.id


class CoffeeShopFood(models.Model):
    _name = 'coffee_shop_food.line'
    _description = 'Coffee Shop Food Service line'
    _inherits = {'sale.order.line': 'coffee_shop_food_line_id'}

    coffee_shop_food_line_id = fields.Many2one('sale.order.line', 'coffee_shop_food_line_id', required=True, ondelete='cascade')
    folio_id = fields.Many2one('hotel.folio', 'Folio', ondelete='cascade')
    source_origin = fields.Char('Source Origin')
    product_uom_qty = fields.Float(string='Quantity', default=0.0)

    @api.model_create_multi
    def create(self, vals_list):
        for rec in vals_list:
            folio = self.env["hotel.folio"].browse(rec['folio_id'])
            if folio:
                rec.update({'order_id': folio.order_id.id})

        res = super(CoffeeShopFood, self).create(vals_list)

        for line in res:
            if not line.price_unit and line.product_id:
                line.price_unit = line.product_id.lst_price

        return res

    @api.onchange('product_id')
    def product_id_change(self):
        self.ensure_one()

        if self.product_id:
            self.product_uom = self.product_id.uom_id
            self.price_unit = self.product_id.lst_price
            self.name = self.product_id.description_sale or self.product_id.name


            if not self.order_id:
                if self.folio_id:
                    self.order_id = self.folio_id.order_id.id


class Minibar(models.Model):
    _name = 'minibar.line'
    _description = 'Minibar Line'
    _inherits = {'sale.order.line': 'minibar_line_id'}

    minibar_line_id = fields.Many2one('sale.order.line', 'minibar_line_id', required=True, ondelete='cascade')
    folio_id = fields.Many2one('hotel.folio', 'Folio', ondelete='cascade')
    source_origin = fields.Char('Source Origin')
    product_uom_qty = fields.Float(string='Quantity', default=0.0)

    @api.model_create_multi
    def create(self, vals_list):
        for rec in vals_list:
            folio = self.env["hotel.folio"].browse(rec['folio_id'])
            if folio:
                rec.update({'order_id': folio.order_id.id})

        res = super(Minibar, self).create(vals_list)

        for line in res:
            if not line.price_unit and line.product_id:
                line.price_unit = line.product_id.lst_price

        return res

    @api.onchange('product_id')
    def product_id_change(self):
        self.ensure_one()

        if self.product_id:
            self.product_uom = self.product_id.uom_id
            self.price_unit = self.product_id.lst_price
            self.name = self.product_id.description_sale or self.product_id.name


            if not self.order_id:
                if self.folio_id:
                    self.order_id = self.folio_id.order_id.id

class BanquetFood(models.Model):
    _name = 'banquet.line'
    _description = 'Banquet Line'
    _inherits = {'sale.order.line': 'banquet_line_id'}

    banquet_line_id = fields.Many2one('sale.order.line', 'banquet_line_id', required=True, ondelete='cascade')
    folio_id = fields.Many2one('hotel.folio', 'Folio', ondelete='cascade')
    source_origin = fields.Char('Source Origin')
    product_uom_qty = fields.Float(string='Quantity', default=0.0)

    @api.model_create_multi
    def create(self, vals_list):
        for rec in vals_list:
            folio = self.env["hotel.folio"].browse(rec['folio_id'])
            if folio:
                rec.update({'order_id': folio.order_id.id})

        res = super(BanquetFood, self).create(vals_list)

        for line in res:
            if not line.price_unit and line.product_id:
                line.price_unit = line.product_id.lst_price

        return res

    @api.onchange('product_id')
    def product_id_change(self):
        self.ensure_one()

        if self.product_id:
            self.product_uom = self.product_id.uom_id
            self.price_unit = self.product_id.lst_price
            self.name = self.product_id.description_sale or self.product_id.name


            if not self.order_id:
                if self.folio_id:
                    self.order_id = self.folio_id.order_id.id


