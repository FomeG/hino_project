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
    x_apply_for_vehicles = fields.Selection([
        ('all', 'All vehicles'),
        ('specific', 'Specific vehicles')
    ], string='Apply for', default='all', tracking=True)

    x_vehicle_ids = fields.Many2many(
        'vehicle.information',  # Model from nhom3_odoo_project
        'x_pricelist_vehicle_rel',
        'pricelist_id',
        'vehicle_id',
        string='Vehicles',
        help="Select vehicles to apply this pricelist to"
    )

    @api.onchange('x_apply_for_vehicles')
    def _onchange_apply_for_vehicles(self):
        """Clear vehicle selection when switching to 'all' vehicles"""
        if self.x_apply_for_vehicles == 'all':
            self.x_vehicle_ids = [(5, 0, 0)]

    @api.constrains('x_apply_for_vehicles', 'x_vehicle_ids')
    def _check_vehicles_required(self):
        """Validate vehicle selection when specific vehicles are chosen"""
        for record in self:
            if record.x_apply_for_vehicles == 'specific' and not record.x_vehicle_ids:
                raise ValidationError(_('Choose at least one vehicle when applying for specific vehicles'))
    @api.constrains('x_from_km', 'x_to_km')
    def _check_km_range(self):
        """Validate kilometer range"""
        for record in self:
            if record.x_from_km and record.x_to_km and record.x_from_km >= record.x_to_km:
                raise ValidationError(_('The starting kilometer must be less than the ending kilometer'))
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