# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Header Information Fields
    name = fields.Char(
        'No',
        required=True,
        readonly=True,
        default=lambda self: _('New'),
        help='Document number with format SO/YYYY/NNNN'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        help='Customer from repair order'
    )

    x_type_of_document = fields.Selection([
        ('parts', 'Parts Sales'),
        ('service', 'Service Sales'),
        ('dropship', 'Dropship Sales'),
        ('repair', 'Repair Order Sales')
    ], string='Document Type', required=True, default='repair')

    partner_shipping_id = fields.Many2one(
        'res.partner',
        string='Delivery Address'
    )

    partner_invoice_id = fields.Many2one(
        'res.partner',
        string='Invoice Address'
    )

    x_deposit = fields.Boolean(
        'Customer Deposit',
        help='Mark if customer made a deposit'
    )

    x_category = fields.Selection([
        ('parts', 'Parts'),
        ('oil', 'Oil'),
        ('service', 'Service')
    ], string='Category', required=True)

    x_type_of_repair_order = fields.Selection([
        ('warranty', 'Warranty'),
        ('maintenance', 'Maintenance'),
        ('spare_part', 'Spare_Parts'),  # Bán phụ tùng
        ('pdi', 'Service')
    ], string='Repair Type')

    pricelist_id = fields.Many2one(
        'product.pricelist',
        string='Pricelist',
        required=True,
        help='Get from repair order x_pricelist_id or customer applicable pricelist'
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id
    )

    currency_rate = fields.Float(
        'Exchange Rate',
        required=True,
        compute='_compute_currency_rate',
        store=True
    )

    date_order = fields.Datetime(
        'Order Date',
        required=True,
        default=fields.Datetime.now
    )

    x_posting_date = fields.Datetime(
        'Posting Date',
        default=fields.Datetime.now
    )

    validity_date = fields.Datetime(
        'Due Date',
        help='Quotation validity date'
    )

    payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Payment Terms'
    )

    origin = fields.Many2one(
        'repair.order',
        string='Source Document',
        help='Reference to originating repair order'
    )

    x_delivery_warehouse = fields.Many2one(
        'stock.warehouse',
        string='Delivery Warehouse'
    )

    description = fields.Text('Description')



    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order', sequence_date=seq_date) or _('New')

        if vals.get('origin'):
            repair_order = self.env['repair.order'].browse(vals['origin'])
            if repair_order:
                # Map repair type to sale order type
                repair_type_mapping = {
                    'warranty': 'warranty',
                    'free_maintenance': 'maintenance',
                    'normal_maintenance': 'maintenance',
                    'free_inspection': 'maintenance',
                    'spare_part': 'spare_part',
                    'pdi': 'pdi'
                }
                quote_type = repair_type_mapping.get(repair_order.x_repair_type)

                vals.update({
                    'partner_id': repair_order.partner_id.id,
                    'x_type_of_document': 'repair',
                    'x_type_of_repair_order': quote_type,
                    'pricelist_id': repair_order.x_pricelist_id.id if repair_order.x_pricelist_id else repair_order.partner_id.property_product_pricelist.id,
                })
        return super(SaleOrder, self).create(vals)

    @api.depends('currency_id')
    def _compute_currency_rate(self):
        for order in self:
            if order.currency_id:
                order.currency_rate = self.env['res.currency.rate'].search([
                    ('currency_id', '=', order.currency_id.id),
                    ('company_id', '=', order.company_id.id)
                ], limit=1).company_rate or 1.0

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        """Update addresses and pricelist when partner changes"""
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'pricelist_id': False
            })
            return

        addr = self.partner_id.address_get(['delivery', 'invoice'])

        # Lấy bảng giá mặc định của khách hàng
        values = {
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            'pricelist_id': self.partner_id.property_product_pricelist.id
        }

        self.update(values)

    @api.onchange('validity_date')
    def _onchange_validity_date(self):
        """Update status based on validity date"""
        if self.validity_date and self.origin:
            if self.origin.x_state != 'repairing':
                self.state = 'cancel'
                self.origin.x_state = 'cancel'

    @api.onchange('date_order')
    def _onchange_date_order(self):
        """Set posting date equal to order date by default"""
        if self.date_order:
            self.x_posting_date = self.date_order

    def action_view_partner_repair_orders(self):
        self.ensure_one()

        # Kiểm tra nếu origin là một record hợp lệ
        if not self.origin or not self.origin.id:
            raise ValidationError("Không tìm thấy chứng từ gốc (Origin) để mở.")

        # Trỏ thẳng đến bản ghi `origin`
        return {
            'type': 'ir.actions.act_window',
            'name': 'Chứng từ gốc',
            'res_model': self.origin._name,
            'view_mode': 'form',
            'res_id': self.origin.id,
            'target': 'main',
        }