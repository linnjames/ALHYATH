from odoo import fields, models


class sale_shop(models.Model):
    """Sale shop inherited for Image"""
    _inherit = "sale.shop"
    _description = "sale shop used for territory name"

    shop_img = fields.Binary("Image", help="This field holds the image for this shop, limited to 1024x1024px")
    wifi = fields.Char('Wifi Password')
    
class sale_line(models.Model):
    """Sale shop inherited for Image"""
    _inherit = "sale.order.line"
    
    def write(self, vals):
        res = super(sale_line ,self).write(vals)
        print("dd")
        return res
