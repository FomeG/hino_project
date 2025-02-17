
# -*- coding: utf-8 -*-

from odoo import models, fields, api



class RepairJobType(models.Model):
    _name = 'repair.job.type'
    _description = 'Repair Job Type'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
