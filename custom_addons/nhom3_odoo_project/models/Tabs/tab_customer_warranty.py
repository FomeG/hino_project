from odoo import models, fields, api, exceptions


class CustomerVehicleInfoInWarranty(models.Model):
    _inherit = 'warranty.request'

    x_engine = fields.Many2one('repair.order', string='Engine', tracking=True)

    x_engine_number = fields.Char(string='Engine Number', tracking=True, related='x_engine.x_engine_number')
    x_main_route = fields.Char(string='Main Route', tracking=True, related='x_engine.x_main_route')
    x_body_type_id = fields.Selection([], string='Body type', tracking=True,
                                      related='x_engine.x_body_type_id')
    x_body_marker = fields.Char(string='Body Marker', tracking=True, related='x_engine.x_body_marker')
    x_trans_number = fields.Char(string='Transmission Number', tracking=True,
                                 related='x_engine.x_trans_number')
    x_customer_delivery_date = fields.Datetime(string='Customer Delivery Time', tracking=True,
                                               related='x_engine.x_customer_delivery_date')

    x_customer_email = fields.Char(string='Customer Email', tracking=True, related='x_engine.x_customer_email')
    x_customer_revenue = fields.Float(string='Customer Revenue', tracking=True, related='x_engine.x_customer_revenue')
