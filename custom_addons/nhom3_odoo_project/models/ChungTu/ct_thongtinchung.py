from odoo import api, fields, models

class CtThongTinChung(models.Model):
    _inherit = 'repair.order'

    # Fields for currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id
    )

    # General Information
    x_customer_feedback = fields.Char(
        string='Customer Feedback',
        help='Customer Feedback'
    )
    x_notes = fields.Char(
        string='Notes',
        help='Notes/Warnings/Recommendations'
    )
    x_content = fields.Char(
        string='Content',
        help='Content'
    )

    x_pricelist_id = fields.Many2one(
        'product.pricelist',
        string='Price List',
        help='Linked Price List'
    )

    # Monetary fields with currency_field specified
    x_total = fields.Monetary(
        string='Subtotal',
        help='Subtotal',
        currency_field='currency_id'
    )
    x_tax_amount = fields.Monetary(
        string='Tax Amount',
        help='Tax Amount',
        currency_field='currency_id'
    )
    x_total_amount = fields.Monetary(
        string='Total',
        help='Total',
        currency_field='currency_id'
    )



    def action_contact(self):
        return

    def action_order_quotations(self):
        return

    def action_export_inv(self):
        return

    def action_customer_care(self):
        return

    def action_feedback(self):
        return

    def action_checkout(self):
        return