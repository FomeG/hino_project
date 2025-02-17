from odoo import models, fields, api

class VehicleOwner(models.Model):
    _inherit = 'repair.order'

    x_vehicle_plate = fields.Many2one('vehicle.information', string="License Plate")
    partner_id = fields.Many2one('res.partner', string="Vehicle Owner", compute="_compute_vehicle_info", store=True)
    x_driver = fields.Char(string='Driver', compute='_compute_vehicle_info', store=True)
    x_driver_phone = fields.Char(string='Driver Phone', compute='_compute_vehicle_info', store=True)

    @api.depends('x_vehicle_plate')
    def _compute_vehicle_info(self):
        """Tự động lấy thông tin chủ xe và lái xe từ biển số"""
        for record in self:
            if record.x_vehicle_plate:
                record.partner_id = record.x_vehicle_plate.owner_info.id
                if record.x_vehicle_plate.driver:
                    record.x_driver = record.x_vehicle_plate.driver.name
                    record.x_driver_phone = record.x_vehicle_plate.driver.mobile
                else:
                    record.x_driver = False
                    record.x_driver_phone = False
            else:
                record.partner_id = False
                record.x_driver = False
                record.x_driver_phone = False