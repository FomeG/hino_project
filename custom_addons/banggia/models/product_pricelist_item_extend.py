# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductPricelistItemExtend(models.Model):
    _inherit = 'product.pricelist.item'

    x_discount_hmv = fields.Float(
        string='Discount HMV',
        digits='Discount',
        default=0.0
    )

    x_discount_dealer = fields.Float(
        string='Discount Dealer',
        digits='Discount',
        default=0.0
    )

    x_discount_value = fields.Float(
        string='Discount value',
        digits='Product Price',
        default=0.0
    )

    x_auto = fields.Boolean(
        string='Auto',
        default=False,
        help="Used to check conditions when creating orders"
    )

    x_allow_update_delete = fields.Boolean(
        string='Allow update/delete',
        default=False,
        help="Allow editing or deleting when creating orders"
    )

    @api.onchange('x_discount_hmv', 'x_discount_dealer')
    def _onchange_discounts(self):
        """Update price_discount when HMV or Dealer discount changes"""
        for record in self:
            record.price_discount = record.x_discount_hmv + record.x_discount_dealer

    @api.constrains('x_discount_hmv', 'x_discount_dealer', 'price_discount')
    def _check_discounts(self):
        """Validate that sum of HMV and Dealer discounts doesn't exceed price_discount"""
        for record in self:
            total_discount = record.x_discount_hmv + record.x_discount_dealer
            if total_discount > record.price_discount:
                raise ValidationError(_('Total of HMV and Dealer discounts cannot exceed the total discount'))