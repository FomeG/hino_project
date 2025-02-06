from odoo import models, fields, api

class ChuXe(models.Model):
    _inherit = 'repair.order'

    x_vehicle_plate = fields.Many2one('vehicle.information', string="License Plate")
    partner_id = fields.Many2one('res.partner', string="Vehicle Owner", compute="_compute_vehicle_owner", store=True)
    x_driver = fields.Char(string="Driver")
    x_driver_phone = fields.Char(string="Driver Phone")

    @api.depends('x_vehicle_plate')
    def _compute_vehicle_owner(self):
        """Tự động lấy chủ xe từ biển số"""
        for record in self:
            if record.x_vehicle_plate:
                record.partner_id = record.x_vehicle_plate.owner_info.id
            else:
                record.partner_id = False

    @api.onchange('x_vehicle_plate')
    def _onchange_vehicle_plate(self):
        """Tự động lấy thông tin lái xe và số điện thoại khi chọn biển số"""
        if self.x_vehicle_plate:
            self.partner_id = self.x_vehicle_plate.owner_info.id
            self.x_driver = self.x_vehicle_plate.driver.name if self.x_vehicle_plate.driver else ''
            self.x_driver_phone = self.x_vehicle_plate.driver_phone if self.x_vehicle_plate.driver_phone else ''