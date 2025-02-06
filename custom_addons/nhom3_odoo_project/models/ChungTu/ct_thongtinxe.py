from odoo import api, fields, models


class ThongTinXe(models.Model):
    _inherit = 'repair.order'

    # Vehicle Information
    x_vehicle_plate = fields.Many2one('vehicle.information', string='License Plate', help='Vehicle license plate from vehicle information')
    x_vehicle_type = fields.Selection([
        ('hino', 'Hino'),
        # Add other types as needed
    ], string='Vehicle Type', default='hino')
    
    x_trademark = fields.Many2one('fleet.vehicle.model.brand', string='Brand', help='Vehicle brand from vehicle information', related='x_vehicle_plate.series_id')
    
    x_vehicle_model = fields.Many2one('fleet.vehicle.model', string='Model', help='Vehicle model from vehicle information', related='x_vehicle_plate.model_list_id')
    x_vin_number = fields.Char(string='VIN Number', help='VIN number from vehicle information', related='x_vehicle_plate.vin')
    
    x_engine_number = fields.Char(string='Engine Number', help='Engine number from vehicle information', related='x_vehicle_plate.engine_number')
    
    x_hmv_maintenance_expiry = fields.Date(string='HMV Maintenance Expiry Date', help='Expiry date from warranty registration')
    
    x_warranty_expiry = fields.Datetime(string='Warranty Expiry Date', help='Warranty expiry date from vehicle information', related='x_vehicle_plate.warranty_expire_date')


