from odoo import models, fields

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    # Related fields for signature
    signed_by = fields.Char(related='sale_order_id.signed_by', string='Signed By', readonly=True)
    signed_on = fields.Datetime(related='sale_order_id.signed_on', string='Signed On', readonly=True)
    signature = fields.Binary(related='sale_order_id.signature', string='Signature', readonly=True)