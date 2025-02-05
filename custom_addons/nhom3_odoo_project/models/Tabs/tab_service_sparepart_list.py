from odoo import api, fields, models
class TabServiceInfo(models.Model):
    _inherit = 'stock.move'

    default_code = fields.Many2one(
        'product.template', 
        string='Part Code',
        domain="[('categ_id.type', '=', 'spare_part')]",
        required=True
    )
    
    x_product_name = fields.Char(
        string='Part Name',
        related='default_code.name',
        readonly=True
    )
    
    product_uom = fields.Many2one(
        'uom.uom',
        string='UoM',
        compute='_compute_product_uom',
        store=True
    )
    
    product_uom_qty = fields.Float(
        string='Quantity',
        required=True
    )
    
    x_pricelist = fields.Many2one(
        'product.pricelist',
        string='Price List',
        required=True
    )
    
    x_unit_price = fields.Float(
        string='Unit Price',
        compute='_compute_unit_price',
        store=True
    )
    
    x_hmv_percent = fields.Float(
        string='% HMV',
        compute='_compute_percentages',
        store=True
    )
    
    x_dealer_percent = fields.Float(
        string='% Dealer',
        compute='_compute_percentages',
        store=True
    )
    
    x_discount = fields.Float(
        string='Discount',
        compute='_compute_discount',
        store=True
    )
    
    x_tax_excluded = fields.Monetary(
        string='Amount',
        compute='_compute_tax_excluded',
        store=True,
        currency_field='currency_id'
    )
    
    x_taxes = fields.Many2one(
        'account.tax',
        string='VAT%',
        required=True
    )
    
    x_tax_amount = fields.Float(
        string='VAT Amount',
        compute='_compute_tax_amount',
        store=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True
    )

    @api.depends('default_code', 'default_code.uom_id')
    def _compute_product_uom(self):
        for record in self:
            if record.default_code:
                record.product_uom = record.default_code.uom_id
    
    @api.depends('default_code', 'x_pricelist')
    def _compute_unit_price(self):
        for record in self:
            if record.default_code and record.x_pricelist:
                price = record.x_pricelist.get_product_price(
                    record.default_code, 1.0, False)
                record.x_unit_price = price
    
    @api.depends('default_code', 'x_pricelist')
    def _compute_percentages(self):
        for record in self:
            if record.default_code and record.x_pricelist:
                record.x_hmv_percent = 0.0
                record.x_dealer_percent = 0.0
    
    @api.depends('default_code', 'x_pricelist')
    def _compute_discount(self):
        for record in self:
            if record.default_code and record.x_pricelist:
                record.x_discount = 0.0
    
    @api.depends('product_uom_qty', 'x_unit_price', 'x_hmv_percent', 'x_dealer_percent', 'x_discount')
    def _compute_tax_excluded(self):
        for record in self:
            base_amount = record.product_uom_qty * record.x_unit_price
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