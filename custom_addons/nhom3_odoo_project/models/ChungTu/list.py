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
        ('confirmed', 'Confirmed'),
        ('repairing', 'Repairing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('created', 'Created'),
    ], string='Satus', default='draft',
        help="* The \'New\' status is used when a user is encoding a new and unconfirmed repair order.\n"
             "* The \'Confirmed\' status is used when a user confirms the repair order.\n"
             "* The \'Under Repair\' status is used when the repair is ongoing.\n"
             "* The \'Repaired\' status is set when repairing is completed.\n"
             "* The \'Cancelled\' status is used when user cancel repair order."
    )

    def button_repair_confirm(self):
        self.x_status = 'confirmed'

    def button_repair_start(self):
        self.x_status = 'repairing'

    def button_repair_end(self):
        self.x_status = 'completed'

    def button_create_sale_order(self):
        self.x_status = 'created'

    def button_repair_cancel(self):
        self.x_status = 'canceled'

    def button_repair_cancel_draft(self):
        self.x_status = 'draft'
