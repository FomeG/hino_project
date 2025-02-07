# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductPricelistKM(models.Model):
    _inherit = 'product.pricelist'

    x_from_km = fields.Float(
        string='Apply for from Km',
        help="Enter the starting kilometer number for application",
        tracking=True
    )

    x_to_km = fields.Float(
        string='To Km',
        help="Enter the ending kilometer number for application",
        tracking=True
    )

    @api.constrains('x_from_km', 'x_to_km')
    def _check_km_range(self):
        """Validate kilometer range"""
        for record in self:
            if record.x_from_km and record.x_to_km and record.x_from_km >= record.x_to_km:
                raise ValidationError(_('The starting kilometer must be less than the ending kilometer'))