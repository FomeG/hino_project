from odoo import models, fields, api

class HoaDonMuaSmartButton(models.Model):
    _inherit = 'account.move'

    # Add counter field for smart button
    x_purchase_invoice_count = fields.Integer(
        string='Purchase Invoice Count',
        compute='_compute_purchase_invoice_count'
    )

    @api.depends('partner_id')
    def _compute_purchase_invoice_count(self):
        for record in self:
            # Count related purchase invoices
            record.x_purchase_invoice_count = self.env['account.move'].search_count([
                ('partner_id', '=', record.partner_id.id),
                ('move_type', '=', 'in_invoice'),
                ('state', '=', 'posted')  # Only count posted/validated invoices
            ])

    def action_view_purchase_invoices(self):
        self.ensure_one()
        return {
            'name': 'Related Purchase Invoices',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [
                ('partner_id', '=', self.partner_id.id),
                ('move_type', '=', 'in_invoice'),
                ('state', '=', 'posted')
            ],
            'context': {'default_move_type': 'in_invoice'},
            'target': 'current',
        }
        
        
        
    def action_hoadonbanhang(self):
        pass
    
    
    
    
    def action_buttoantonghop(self):
        pass