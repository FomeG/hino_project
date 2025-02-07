# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductPricelistDL(models.Model):
    _inherit = 'product.pricelist'

    x_apply_for_dealer = fields.Selection([
        ('all', 'All dealers'),
        ('specific', 'Specific dealers')
    ], string='Apply for', default='all', tracking=True)

    x_dealer_ids = fields.Many2many(
        'res.company',
        'x_pricelist_dealer_rel',
        'pricelist_id',
        'company_id',
        string='Dealers',
        help="Select dealers to apply this pricelist to",
        # domain="[('is_dealer', '=', True)]"  # Assuming there's a field to identify dealers
    )

    @api.onchange('x_apply_for_dealer')
    def _onchange_apply_for_dealer(self):
        """Clear dealer selection when switching to 'all' dealers"""
        if self.x_apply_for_dealer == 'all':
            self.x_dealer_ids = [(5, 0, 0)]

    @api.constrains('x_apply_for_dealer', 'x_dealer_ids')
    def _check_dealer_required(self):
        """Validate dealer selection when specific dealers are chosen"""
        for record in self:
            if record.x_apply_for_dealer == 'specific' and not record.x_dealer_ids:
                raise ValidationError(_('Choose at least one dealer when applying for specific dealers'))