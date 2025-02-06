from odoo import fields, models, api


class ListView(models.Model):
    _inherit = 'repair.order'

    x_quotation_id = fields.Char(string='Quotation Name')
    x_appointment_status = fields.Selection([
        ('draft', 'Unconfirmed'),
        ('open', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Appointment Status", default='draft')
    x_status = fields.Selection([
        ('draft', 'Draft'),
        ('repairing', 'Repairing'),
        ('completed', 'Completed'),
        ('cancel', 'Canceled'),
        ('created', 'Created'),
    ], string='Satus', default='draft')
