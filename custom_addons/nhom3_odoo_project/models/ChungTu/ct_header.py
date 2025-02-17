# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class CtHeader(models.Model):
    _inherit = 'repair.order'

    # Override name field to make it required and readonly
    name = fields.Char('Repair Reference', required=True, readonly=True, default='/')

    # Repair Type
    x_repair_type = fields.Selection([
        ('warranty', 'Warranty repairs'),
        ('free_maintenance', 'Free maintenance'),
        ('normal_maintenance', 'Normal maintenance'),
        ('free_inspection', 'Free inspection'),
        ('spare_part', 'Spare part sales'),
        ('pdi', 'PDI')
    ], string='Repair Type', required=True)

    # Appointment
    x_schedule_id = fields.Many2one('calendar.event', string='Appointment')

    # CPUS Status 
    x_cpus_status = fields.Selection([
        ('cpus', 'CPUS'),
        ('non_cpus', 'Non CPUS')
    ], string='CPUS Status')

    # Repair Action
    x_repair_action = fields.Selection([
        ('new', 'New Repair'),
        ('redo', 'Redo Repair')
    ], string='Repair Action')

    # Repair Result
    x_repair_result = fields.Selection([
        ('pass', 'Pass'),
        ('pass_with_warning', 'Pass with Warning'),
        ('fail', 'Fail')
    ], string='Result')

    # Service Advisor
    x_service_advisor_id = fields.Many2one('res.users', string='Service Advisor',
                                           default=lambda self: self.env.user)

    # Times
    x_entry_time = fields.Datetime('Entry Time')
    x_reception_time = fields.Datetime('Reception Time')
    x_expected_completion_time = fields.Datetime('Expected Completion Time')
    x_completion_time = fields.Datetime('Completion Time', readonly=True)

    # KM at repair
    x_km_at_repair = fields.Float('KM at Repair')

    # Execution Location
    x_execution_location = fields.Selection([
        ('outside', 'Outside Station'),
        ('inside', 'Inside Station')
    ], string='Execution Location', default='inside')

    @api.constrains('x_km_at_repair')
    def _check_km_at_repair(self):
        """ Ensure KM at repair is not negative """
        for record in self:
            if record.x_km_at_repair < 0:
                raise ValidationError(_("Kilometers at repair cannot be negative."))

    @api.constrains('x_schedule_id', 'x_repair_type')
    def _check_appointment_required(self):
        """ Ensure an appointment is set for certain repair types """
        for record in self:
            if record.x_repair_type in ['warranty', 'free_maintenance',
                                        'normal_maintenance'] and not record.x_schedule_id:
                raise ValidationError(_("An appointment is required for repair type: %s" % record.x_repair_type))

    @api.model
    def create(self, vals):
        """ Validate required fields before creating a record """
        required_fields = ['x_repair_type', 'x_entry_time', 'x_service_advisor_id', 'x_execution_location']
        for field_name in required_fields:
            if field_name not in vals or not vals[field_name]:
                raise ValidationError(
                    _("%s is required to create a repair record." % field_name.replace('_', ' ').title()))

        return super(CtHeader, self).create(vals)

    def write(self, vals):
        if vals.get('state') == 'done':
            vals['x_completion_time'] = fields.Datetime.now()
            missing_fields = []
            if not self.x_cpus_status:
                missing_fields.append("CPUS Status")
            if not self.x_repair_action:
                missing_fields.append("Repair Action")
            if not self.x_repair_result:
                missing_fields.append("Repair Result")

            if missing_fields:
                raise ValidationError(
                    _("The following fields must be filled before completing the repair: %s") % ", ".join(
                        missing_fields))

        return super(CtHeader, self).write(vals)
