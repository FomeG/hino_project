# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductPricelistItemExtend(models.Model):
    _inherit = 'product.pricelist.item'

    # Custom fields với prefix x_
    x_discount_hmv = fields.Float(
        string='HMV Discount (%)',
        digits='Discount',
        default=0.0,
        help="Discount percentage for HMV"
    )

    x_discount_dealer = fields.Float(
        string='Dealer Discount (%)', 
        digits='Discount',
        default=0.0,
        help="Discount percentage for Dealer"
    )

    x_discount_value = fields.Float(
        string='Discount Value',
        digits='Product Price',
        default=0.0,
        help="Discount amount in currency"
    )

    x_auto = fields.Boolean(
        string='Auto',
        default=False,
        help="Used to check conditions when creating orders"
    )

    x_allow_update_delete = fields.Boolean(
        string='Allow Update/Delete',
        default=False,
        help="Allow editing or deleting when creating orders"
    )

    price_discount = fields.Float(
        string="Total Discount (%)",
        compute='_compute_price_discount',
        store=True,
        readonly=True,
        help="Total discount percentage (HMV + Dealer)"
    )

    @api.depends('x_discount_hmv', 'x_discount_dealer')
    def _compute_price_discount(self):
        """Compute total discount from HMV and Dealer discounts"""
        for record in self:
            record.price_discount = record.x_discount_hmv + record.x_discount_dealer

    @api.constrains('x_discount_hmv', 'x_discount_dealer')
    def _check_discounts(self):
        """Validate discount values"""
        for record in self:
            if record.x_discount_hmv < 0:
                raise ValidationError(_('HMV Discount cannot be negative'))
            if record.x_discount_dealer < 0:
                raise ValidationError(_('Dealer Discount cannot be negative'))
