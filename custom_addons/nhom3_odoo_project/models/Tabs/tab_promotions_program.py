from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class PromotionProgram(models.Model):
    _inherit = 'repair.order'

    x_vehicle_plate = fields.Many2one('vehicle.information', string='License Plate', required=True)
    x_km_at_repair = fields.Float(string='KM at Repair', required=True, help='Current mileage of the vehicle at the time of repair')
    x_pricelist_id = fields.Many2one(
        'product.pricelist',
        string='Price List',
        compute='_compute_applicable_pricelist',
        store=True,
        help='Price list applicable for the repair order'
    )

    @api.depends('partner_id', 'x_vehicle_plate', 'x_km_at_repair')
    def _compute_applicable_pricelist(self):
        """
        Compute the applicable price list based on:
        - Customer (partner_id)
        - Vehicle (x_vehicle_plate)
        - Current mileage (x_km_at_repair)
        """
        for record in self:
            # Initialize domain for pricelist search
            domain = ['|',
                     '|',
                     # Customer conditions
                     '&',
                     ('x_apply_for', '=', 'specific'),
                     ('x_customer_ids', 'in', record.partner_id.id),
                     # Vehicle conditions
                     '&',
                     ('x_apply_for_vehicles', '=', 'specific'),
                     ('x_vehicle_ids', 'in', record.x_vehicle_plate.id),
                     # Kilometer conditions
                     '&',
                     ('x_from_km', '<=', record.x_km_at_repair),
                     '|',
                     ('x_to_km', '=', 0),
                     ('x_to_km', '>=', record.x_km_at_repair)]

            # Search for applicable pricelist
            pricelist = self.env['product.pricelist'].search(
                domain,
                order='create_date desc',
                limit=1
            )

            record.x_pricelist_id = pricelist.id if pricelist else False

    @api.constrains('x_km_at_repair')
    def _check_km_at_repair(self):
        """Validate repair kilometer value"""
        for record in self:
            if record.x_km_at_repair < 0:
                raise ValidationError(_('Repair kilometer cannot be negative'))