from odoo import api, fields, models

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    applies_to_customer = fields.Many2one('res.partner', string='Áp dụng cho khách hàng')
    applies_to_vehicle = fields.Many2one('fleet.vehicle', string='Áp dụng cho xe')
    applies_to_km = fields.Float(string='Áp dụng theo số Km')