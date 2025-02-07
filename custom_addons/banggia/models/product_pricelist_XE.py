# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

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