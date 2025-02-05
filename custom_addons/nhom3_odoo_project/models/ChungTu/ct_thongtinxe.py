from odoo import api, fields, models


class ThongTinXe(models.Model):
    _inherit = 'repair.order'

    # Vehicle Information
    x_vehicle_plate = fields.Many2one('fleet.vehicle', string='License Plate', required=True,
                                    help='Vehicle license plate from vehicle information')
    x_vehicle_type = fields.Selection([
        ('hino', 'Hino'),
        # Add other types as needed
    ], string='Vehicle Type', required=True, default='hino')
    
    x_trademark = fields.Many2one('fleet.vehicle.model.brand', string='Brand', required=True,
                                help='Vehicle brand from vehicle information')
    
    x_vehicle_model = fields.Many2one('fleet.vehicle.model', string='Model', required=True,
                                    help='Vehicle model from vehicle information')
    x_vin_number = fields.Many2one('fleet.vehicle', string='VIN Number', required=True,
                                  help='VIN number from vehicle information')
    
    x_engine_number = fields.Many2one('fleet.vehicle', string='Engine Number', required=True,
                                    help='Engine number from vehicle information')
    
    x_hmv_maintenance_expiry = fields.Date(string='HMV Maintenance Expiry Date', required=True,
                                         help='Expiry date from warranty registration')
    
    x_warranty_expiry = fields.Date(string='Warranty Expiry Date', required=True,
                                  help='Warranty expiry date from vehicle information')

    @api.onchange('x_vin_number')
    def _onchange_vin_number(self):
        if self.x_vin_number:
            vehicle = self.x_vin_number
            self.x_vehicle_plate = vehicle.id
            self.x_trademark = vehicle.brand_id.id
            self.x_vehicle_model = vehicle.model_id.id
            self.x_engine_number = vehicle.id
            self.x_warranty_expiry = vehicle.warranty_expiry_date
