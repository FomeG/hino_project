# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductPricelistKH(models.Model):
    _inherit = 'product.pricelist'

    x_apply_for = fields.Selection([
        ('all', 'All customers'),
        ('specific', 'Specific customer')
    ], string='Apply for', default='all', tracking=True)

    x_customer_ids = fields.Many2many(
        'res.partner',
        'x_pricelist_partner_rel',
        'pricelist_id',
        'partner_id', 
        string='Customer',
        domain="[('customer_rank', '>', 0)]",
        help="Chọn khách hàng để áp dụng bảng giá này"
    )

    @api.onchange('x_apply_for') 
    def _onchange_apply_for(self):
        """Clear customer selection when switching to 'all' customers"""
        if self.x_apply_for == 'all':
            self.x_customer_ids = [(5, 0, 0)]

    @api.constrains('x_apply_for', 'x_customer_ids')
    def _check_customer_required(self):
        """Validate customer selection when specific customers are chosen"""
        for record in self:
            if record.x_apply_for == 'specific' and not record.x_customer_ids:
                raise ValidationError(_('Choose at least one customer when applying for specific customer'))