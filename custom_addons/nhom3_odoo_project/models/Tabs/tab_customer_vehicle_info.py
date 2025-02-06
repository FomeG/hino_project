from odoo import models, fields, api, exceptions


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
