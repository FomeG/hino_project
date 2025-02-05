from odoo import models, fields, api

class ChuXe(models.Model):
    _inherit = 'repair.order'

    # header chứng từ chủ xe
    partner_id = fields.Many2one('res.partner', string="Vehicle Owner")
    x_driver = fields.Char(string="Driver")
    x_driver_phone = fields.Char(string="Driver Phone")
