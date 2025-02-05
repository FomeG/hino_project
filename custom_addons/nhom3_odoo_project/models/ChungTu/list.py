from odoo import fields, models, api


class ListView(models.Model):
    _inherit = 'repair.order'

    x_quotation_id = fields.Char(string='Quotation Name')
    # x_appointment_status = fields.Char(string="Trạng thái đặt hẹn", compute="_compute_x_appointment_status", store=True)
    x_appointment_status = fields.Selection([
        ('draft', 'Unconfirmed'),
        ('open', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Appointment Status", compute="_compute_x_appointment_status", store=True)
    x_status = fields.Selection([
        ('draft', 'Draft'),
        ('repairing', 'Repairing'),
        ('completed', 'Completed'),
        ('cancel', 'Canceled'),
        ('created', 'Created'),
    ], string='Satus', default='draft')

    @api.depends('x_schedule_id', 'x_schedule_id.current_status')
    def _compute_x_appointment_status(self):
        for record in self:
            record.x_appointment_status = record.x_schedule_id.current_status if record.x_schedule_id else ""

