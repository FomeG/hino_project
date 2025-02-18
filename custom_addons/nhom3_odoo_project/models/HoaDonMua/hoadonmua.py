from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountMove_Nghia(models.Model):
    _inherit = 'account.move'
    x_dealer = fields.Many2one(
        'res.users', 
        string='Dealer',
        domain="[('company_ids', 'in', company_id)]",
        required=True
    )
    
    x_category = fields.Many2one(
        'product.category',
        string='Category',
        required=True
    )
    
    # x_type_of_order = fields.Many2one(
    #     'purchase.order.type',
    #     string='Type of order',
    #     required=True
    # )
    
    x_bill_number = fields.Char(
        string='Bill number'
    )
    
    x_form = fields.Char(
        string='Form'
    )
    
    x_serial = fields.Char(
        string='Serial'
    )
    
    x_description = fields.Text(
        string='Description'
    )
    
    x_source_document = fields.Char(
        string='Source Document',
        readonly=True
    )
    
    x_currency = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    
    x_currency_rate = fields.Many2one(
        'res.currency.rate',
        string='Currency Rate',
    )
    
    
    # x_currency_rate = fields.Float(
    #     string='Currency Rate',
    #     digits=(12, 6),  # 6 decimal places precision
    #     default=1.0
    # )
    
    x_type_of_vendor_bill = fields.Selection([
        ('normal', 'Normal'),
        ('cashback', 'Cashback')
    ], string='Type of Vendor Bill', default='normal')
    
    
    
    purchase_order_ids = fields.Many2many(
        'purchase.order',
        string='Purchase Order',
        required=True
    )
    x_approval_attachment_file = fields.Binary(string="Approval Information")
    x_approval_attachment_filename = fields.Char(string="Approval Information File Name")

    x_attachment_file = fields.Binary(string="Attachment")
    x_attachment_filename = fields.Char(string="Attachment File Name")
    def create(self, vals):
        # Chỉ tạo sequence cho vendor bill mới
        if vals.get('move_type') == 'in_invoice' and vals.get('name', '/') == '/':
            if self.env['account.move'].search([('move_type', '=', 'in_invoice')], limit=1):
                sequence = self.env['ir.sequence'].next_by_code('vendor.bill.sequence')
                if sequence:
                    vals['name'] = sequence
                else:
                    today = fields.Date.context_today(self)
                    vals['name'] = f'BILL/{today.year}/0001'
            else:
                # Nếu là record đầu tiên
                today = fields.Date.context_today(self)
                vals['name'] = f'BILL/{today.year}/0001'
                
        return super().create(vals)

    def copy(self, default=None):
        # Đảm bảo khi duplicate record sẽ lấy sequence mới
        default = dict(default or {})
        default['name'] = '/'
        return super().copy(default)
    
    
    state = fields.Selection(selection_add=[
        ('approval', 'Waiting Approval'),
        ('approved', 'Approved'),
        ('done', 'Done')
    ], ondelete={
        'approval': 'cascade',
        'approved': 'cascade', 
        'done': 'cascade'
    })
        
        
        
    # @api.onchange('purchase_order_ids') 
    # def _onchange_purchase_orders(self):
    #     if self.purchase_order_ids:
    #         first_po = self.purchase_order_ids[0]
    #         # Kiểm tra giá trị tồn tại trước khi gán
    #         if hasattr(first_po, 'x_category') and first_po.x_category:
    #             self.x_category = first_po.x_category.id
    #         if hasattr(first_po, 'x_type_of_order') and first_po.x_type_of_order:
    #             self.x_type_of_order = first_po.x_type_of_order.id
    #         # Chỉ gán source_document khi có purchase orders
    #         po_names = self.purchase_order_ids.mapped('name')
    #         if po_names:
    #             self.x_source_document = ', '.join(po_names)
                
                

    
    def action_approval_submission(self):
        self.write({'state': 'approval'})

    def action_cancel(self):
        return
        # self.write({'state': 'cancel'})

    def action_print(self):
        return self.env.ref('account.account_invoices').report_action(self)

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_denial(self):
        self.write({'state': 'draft'})
    
    
    
    
    
    def action_payment_approval(self):
        pass
    
    
    
    
    def ac_cancel(self):
        pass