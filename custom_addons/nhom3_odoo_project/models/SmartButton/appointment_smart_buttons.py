from odoo import api, fields, models


class AppointmentSmartButtons(models.Model):
    _inherit = 'calendar.event'

    x_repair_order_count = fields.Integer(compute='_compute_repair_order_count')

    def _compute_repair_order_count(self):
        for record in self:
            record.x_repair_order_count = self.env['repair.order'].search_count([('x_schedule_id', '=', record.id)])

    def action_open_repair_orders(self):
        return {
            'name': 'Repair Order',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'repair.order',
            'domain': [('x_schedule_id', '=', self.id)],
            'context': {'create': False},
            'target': 'current',
        }
