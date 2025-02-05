from odoo import api, fields, models
from datetime import datetime

class TabServiceInfoDocument(models.Model):
    _inherit = 'stock.move'

    # Work List Details Fields
    x_repair_order = fields.Many2one('repair.order', string='Repair Order', required=True)
    x_task_name = fields.Many2one('product.template', string='Task Name', required=True)
    x_main_responsible = fields.Many2one('res.users', string='Main Responsible', required=True)
    x_work_area = fields.Selection([
        ('khoang1', 'Khoang 1'),
        ('khoang2', 'Khoang 2'),
        ('khoang3', 'Khoang 3'),
        ('khoang4', 'Khoang 4')
    ], string='Khoang', required=True)
    x_standard_hours = fields.Float(string='Standard Hours', required=True)
    x_start_time = fields.Datetime(string='Start Time', required=True)
    x_end_time = fields.Datetime(string='End Time', required=True)
    x_actual_hours = fields.Float(string='Actual Hours', compute='_compute_actual_hours', store=True)

    @api.depends('x_start_time', 'x_end_time')
    def _compute_actual_hours(self):
        for record in self:
            if record.x_start_time and record.x_end_time:
                # Calculate hours difference between end and start time
                delta = record.x_end_time - record.x_start_time
                record.x_actual_hours = delta.total_seconds() / 3600.0
            else:
                record.x_actual_hours = 0.0

    # Override default value for repair_line_type
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'repair_line_type' not in vals:
                vals['repair_line_type'] = 'add'
        return super().create(vals_list)