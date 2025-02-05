from odoo import api, fields, models

class TabServiceInfoWorklistService(models.Model):
    _inherit = 'stock.move'

    # Service Information Fields
    x_default_code = fields.Many2one('product.template', string='Work', required=True,
        domain="[('detailed_type', '=', 'service')]")
    
    x_service_description = fields.Char(
        string='Work Description',
        related='x_default_code.name',
        readonly=True,
        required=True
    )
    
    x_task_details = fields.Char(
        string='Work Details'
    )
    
    x_performer = fields.Char(
        string='Performer'
    )
    
    x_work_hours = fields.Float(
        string='Work Hours',
        required=True
    )
    
    x_outsource = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External')
    ], string='Outsource')
    
    x_pricelist = fields.Many2one(
        'product.pricelist',
        string='Price List',
        required=True
    )
    
    x_quantity = fields.Float(
        string='Quantity',
        required=True,
        default=1.0
    )
    
    x_unit_price = fields.Float(
        string='Unit Price',
        compute='_compute_unit_price',
        store=True,
        required=True
    )
    
    x_hmv_percent = fields.Float(
        string='%HMV',
        compute='_compute_percentages',
        store=True,
        required=True
    )
    
    x_dealer_percent = fields.Float(
        string='%Dealer',
        compute='_compute_percentages',
        store=True,
        required=True
    )
    
    x_task_count = fields.Integer(
        string='Work Count',
        required=True,
        default=1
    )
    
    x_discount = fields.Float(
        string='Discount',
        compute='_compute_discount',
        store=True,
        required=True
    )
    
    x_tax_excluded = fields.Monetary(
        string='Amount',
        compute='_compute_tax_excluded',
        store=True,
        currency_field='currency_id',
        required=True
    )
    
    x_taxes = fields.Many2one(
        'account.tax',
        string='VAT%',
        required=True
    )
    
    x_tax_amount = fields.Float(
        string='VAT Amount',
        compute='_compute_tax_amount',
        store=True,
        required=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    # Compute methods
    @api.depends('x_default_code', 'x_pricelist')
    def _compute_unit_price(self):
        for record in self:
            if record.x_default_code and record.x_pricelist:
                record.x_unit_price = record.x_pricelist.get_product_price(
                    record.x_default_code, 1.0, False)
    
    @api.depends('x_default_code', 'x_pricelist')
    def _compute_percentages(self):
        for record in self:
            if record.x_default_code and record.x_pricelist:
                record.x_hmv_percent = record.x_pricelist.get_hmv_percent(record.x_default_code)
                record.x_dealer_percent = record.x_pricelist.get_dealer_percent(record.x_default_code)
    
    @api.depends('x_default_code', 'x_pricelist')
    def _compute_discount(self):
        for record in self:
            if record.x_default_code and record.x_pricelist:
                record.x_discount = record.x_pricelist.get_discount(record.x_default_code)
    
    @api.depends('x_quantity', 'x_unit_price', 'x_hmv_percent', 'x_dealer_percent', 'x_discount')
    def _compute_tax_excluded(self):
        for record in self:
            base_amount = record.x_quantity * record.x_unit_price
            hmv_discount = base_amount * (record.x_hmv_percent / 100)
            dealer_discount = base_amount * (record.x_dealer_percent / 100)
            record.x_tax_excluded = base_amount - hmv_discount - dealer_discount - record.x_discount
    
    @api.depends('x_tax_excluded', 'x_taxes')
    def _compute_tax_amount(self):
        for record in self:
            if record.x_taxes:
                record.x_tax_amount = record.x_tax_excluded * (record.x_taxes.amount / 100)
            else:
                record.x_tax_amount = 0.0