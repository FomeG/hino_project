from odoo import fields, models, api

class SmartButtons(models.Model):
    _inherit = 'repair.order'

    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count")

    # Contact smart button
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['calendar.event'].search_count([('id', '=', record.x_schedule_id.id)])

    def action_contact(self):
        return {
            'name': 'Contact',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'calendar.event',
            'domain': [('id', '=', self.x_schedule_id.id)],
            'context': {'create': False},
        }

    # Order quotations smart button
    def action_order_quotations(self):
        return

    # Export inventory smart button
    def action_export_inv(self):
        return

    # Customer care smart button
    def action_customer_care(self):
        return

    # Customer complaint smart button
    def action_complaint(self):
        return

    def action_checkout(self):
        return

