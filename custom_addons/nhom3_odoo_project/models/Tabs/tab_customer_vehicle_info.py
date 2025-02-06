from odoo import models, fields, api


class CustomerVehicleInfo(models.Model):
    _inherit = 'repair.order'

    x_engine_number = fields.Char(string='Engine Number', tracking=True)
    x_main_route = fields.Char(string='Main Route', tracking=True)
    x_body_type_id = fields.Char(string='Body Type', tracking=True)
    x_body_marker = fields.Char(string='Body Marker', tracking=True)
    x_trans_number = fields.Char(string='Transmission Number', tracking=True)
    x_customer_delivery_date = fields.Datetime(string='Customer Delivery Time', tracking=True)
    x_customer_email = fields.Char(string='Customer Email', tracking=True, related='partner_id.email')
    x_customer_revenue = fields.Float(string='Customer Revenue', tracking=True, compute='_compute_customer_revenue')

    def _compute_customer_revenue(self):
        self.x_customer_revenue = 0.0
