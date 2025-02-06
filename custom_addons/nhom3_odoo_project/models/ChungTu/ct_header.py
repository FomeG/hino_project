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

    @api.model
    def create(self, vals):
        return super(CtHeader, self).create(vals)

    def write(self, vals):
        if vals.get('state') == 'done':
            vals['x_completion_time'] = fields.Datetime.now()
            if not (self.x_cpus_status and self.x_repair_action and self.x_repair_result):
                raise ValidationError(_("CPUS Status, Repair Action and Repair Result are required to complete repair2222"))
        return super(CtHeader, self).write(vals)