from odoo import models, fields, api, exceptions

from odoo.exceptions import ValidationError

class CustomerVehicleInfo(models.Model):
    _inherit = 'repair.order'

    x_engine_number = fields.Char(string='Engine Number', tracking=True)
    x_main_route = fields.Char(string='Main Route', tracking=True)
    x_body_type_id = fields.Selection([], string='Body type', tracking=True, related='x_vehicle_plate.body_type_id')
    x_body_marker = fields.Char(string='Body Marker', tracking=True, related='x_vehicle_plate.body_marker')
    x_trans_number = fields.Char(string='Transmission Number', tracking=True, related='x_vehicle_plate.trans_number')
    x_customer_delivery_date = fields.Datetime(string='Customer Delivery Time', tracking=True, related='x_entry_time')

    x_customer_email = fields.Char(string='Customer Email', tracking=True, related='partner_id.email')
    x_customer_revenue = fields.Float(string='Customer Revenue', tracking=True, compute='_compute_customer_revenue')

    def _compute_customer_revenue(self):
        self.x_customer_revenue = 0.0

    @api.constrains('x_vehicle_plate', 'partner_id')
    def _check_vehicle_owner(self):
        for record in self:
            if record.x_vehicle_plate and record.partner_id and record.x_vehicle_plate.owner_info != record.partner_id:
                raise exceptions.ValidationError(
                    "This owner does not match the vehicle owner!"
                )
    x_vehicle_plate = fields.Many2one('vehicle.information', string='Vehicle Information', required=True)
    x_km_at_repair = fields.Float(string='KM at Repair', required=True)
    x_pricelist_id = fields.Many2one(
        'product.pricelist',
        string='Price List',
        compute='_compute_applicable_pricelist',
        store=True
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

    @api.onchange('x_vehicle_plate')
    def _onchange_vehicle_plate(self):
        """Update partner when vehicle information changes"""
        if self.x_vehicle_plate:
            self.partner_id = self.x_vehicle_plate.owner_info

    @api.constrains('x_km_at_repair')
    def _check_km_at_repair(self):
        """Validate repair kilometer value"""
        for record in self:
            if record.x_km_at_repair < 0:
                raise ValidationError(('Repair kilometer cannot be negative'))
            

    # Fields for repair history
    repair_order_id = fields.Many2one('repair.order', string='Số lệnh sửa chữa')
    job_type = fields.Many2one('repair.job.type', string='Loại công việc')


    
    #customer_signature
    require_signature = fields.Boolean(string='Require Signature', default=True)
    signed_by = fields.Char(string='Signed By')
    signed_on = fields.Datetime(string='Signed On')
    signature = fields.Binary(string='Signature', attachment=True)