
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RepairHistory(models.Model):
    _inherit = 'repair.order'

    # Fields for repair history
    repair_order_id = fields.Many2one('repair.order', string='Số lệnh sửa chữa')
    job_type = fields.Many2one('repair.job.type', string='Loại công việc')

class RepairJobType(models.Model):
    _name = 'repair.job.type'
    _description = 'Repair Job Type'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
