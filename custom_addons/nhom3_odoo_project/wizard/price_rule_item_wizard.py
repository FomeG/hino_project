# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class PriceRuleWizard(models.TransientModel):  # Đổi từ Model thành TransientModel
    _name = 'price.rule.wizard'  # Đặt _name riêng cho wizard
    _description = 'Price Rule Wizard'

    # Fields for price computation
    computation = fields.Selection([
        ('fixed', 'Fixed Price'),
        ('percentage', 'Percentage (discount)'),
        ('formula', 'Formula')
    ], string='Computation', required=True, default='fixed')

    base = fields.Selection([
        ('list_price', 'Sales Price'),
        ('standard_price', 'Cost Price'),
        ('pricelist', 'Other Pricelist')
    ], string='Based On', required=True, default='list_price')

    x_discount_hmv = fields.Float(string='HMV Discount (%)', digits='Discount', default=0.0)
    x_discount_dealer = fields.Float(string='Dealer Discount (%)', digits='Discount', default=0.0)
    x_discount_value = fields.Float(string='Discount Value', digits='Product Price', default=0.0)
    x_extra_fee = fields.Float(string='Extra Fee', digits='Product Price', default=0.0)
    
    price_round = fields.Float('Price Rounding', digits='Product Price')
    price_min_margin = fields.Float('Min. Margin', digits='Product Price')
    price_max_margin = fields.Float('Max. Margin', digits='Product Price')

    # Fields for conditions
    applied_on = fields.Selection([
        ('3_global', 'All Products'),
        ('2_product_category', 'Product Category'),
        ('1_product', 'Product'),
        ('0_product_variant', 'Product Variant')
    ], string='Apply On', required=True, default='3_global')

    
    
    
    
    
    
    product_tmpl_id = fields.Many2one(
        'product.template',
        'Product',
        ondelete='cascade',
        help="Specify a template if this rule only applies to one product template."
    )
    product_id = fields.Many2one('product.product', 'Variants', ondelete='cascade')
    categ_id = fields.Many2one(
        'product.category', 
        'Product Category',
        ondelete='cascade',
        help="Specify a product category if this rule only applies to products belonging to this category or its children categories."
    )
    
    
    
    
    
    
    min_quantity = fields.Float('Min. Quantity', defaults=0)
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
    
    currency_id = fields.Many2one('res.currency', 'Currency')
    company_id = fields.Many2one('res.company', 'Company')
    
    pricelist_id = fields.Many2one('product.pricelist', string='Price List', required=True)

    @api.model
    def default_get(self, fields):
        res = super(PriceRuleWizard, self).default_get(fields)
        if self._context.get('active_id'):
            pricelist = self.env['product.pricelist'].browse(self._context.get('active_id'))
            res.update({
                'pricelist_id': pricelist.id,
                'currency_id': pricelist.currency_id.id,
                'company_id': pricelist.company_id.id,
            })
        return res



    @api.onchange('applied_on')
    def _onchange_applied_on(self):
        """Clear values when application scope changes"""
        if self.applied_on != '0_product_variant':
            self.product_id = False
        if self.applied_on != '1_product':
            self.product_tmpl_id = False
        if self.applied_on != '2_product_category':
            self.categ_id = False


    def action_confirm(self):
        self.ensure_one()
        # Tạo price rule mới
        vals = {
            'pricelist_id': self.pricelist_id.id,
            'applied_on': self.applied_on,
            'compute_price': self.computation,
            'base': self.base,
            'x_discount_hmv': self.x_discount_hmv,
            'x_discount_dealer': self.x_discount_dealer,
            'x_discount_value': self.x_discount_value,
            'min_quantity': self.min_quantity,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'currency_id': self.currency_id.id,
            'company_id': self.company_id.id,
        }
        # Thêm product_id hoặc product_tmpl_id tùy theo applied_on
        if self.applied_on == '0_product_variant' and self.product_id:
            vals['product_id'] = self.product_id.id
        elif self.applied_on == '1_product' and self.product_tmpl_id:
            vals['product_tmpl_id'] = self.product_tmpl_id.id
        elif self.applied_on == '2_product_category' and self.categ_id:
            vals['categ_id'] = self.categ_id.id
            
            
            
        # Tạo price rule mới
        self.env['product.pricelist.item'].create(vals)
        return {'type': 'ir.actions.act_window_close'}
