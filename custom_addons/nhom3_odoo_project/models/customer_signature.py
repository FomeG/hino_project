from odoo import models, fields

class RepairOrder_signature(models.Model):
    _inherit = 'repair.order'

    require_signature = fields.Boolean(string='Require Signature', default=True)
    signed_by = fields.Char(string='Signed By')
    signed_on = fields.Datetime(string='Signed On')
    signature = fields.Binary(string='Signature', attachment=True)