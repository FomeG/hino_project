from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)

    # default_code = fields.Many2one('product.template', string="Product Code", domain="[('categ_id.name', 'in', ['Phụ tùng', 'Dầu nhớt'])]")
    # replacing_code = fields.Char(string="Replacing Code", related="product_id.replacing_code")
    
    product_id = fields.Many2one("product.product", string="Product")  # Liên kết với Product

    product_name = fields.Char(string="Product Name", related="product_id.name")
    # other_name = fields.Char(string="Other Name", related="product_id.other_name")
    description = fields.Text(string="Description", default=lambda self: self.order_id.note)
    product_uom_qty = fields.Float(string="Quantity", required=True)
    qty_delivered = fields.Float(
            string="Delivered",
            readonly=True,
            compute="_compute_qty_delivered",
            store=True
        )
    qty_invoiced = fields.Float(
            string="Invoiced", 
            readonly=True, 
            compute="_compute_qty_invoiced", 
            store=True
        )
    product_uom = fields.Many2one('uom.uom', string="UoM", required=True)
    pricelist_id = fields.Many2one('product.pricelist', string="Pricelist")
    price_unit = fields.Float(
            string="Unit Price",
            required=True,
            compute="_compute_price_unit",
            store=True
        )
    delivery_warehouse = fields.Many2one('stock.location', string="Delivery Warehouse")
    percent_hmv = fields.Float(string="% HMV")
    percent_dealer = fields.Float(string="% Dealer")
    discount = fields.Float(string="Discount")
    tax_id = fields.Many2many('account.tax', string="Taxes")
    price_subtotal = fields.Monetary(string="Tax Excluded", compute="_compute_price_subtotal")
    untaxed_amount = fields.Monetary(string="Untaxed Amount", compute="_compute_untaxed_amount")
    taxes = fields.Monetary(string="Taxes", compute="_compute_taxes", store=True)
    total = fields.Monetary(string="Total", compute="_compute_total")
    #
    @api.depends('order_id.picking_ids.state')
    def _compute_qty_delivered(self):
        for line in self:
            # Kiểm tra xem có phiếu xuất kho nào đã xác nhận không
            pickings = line.order_id.picking_ids.filtered(lambda p: p.state == 'done')
            if pickings:
                line.qty_delivered = line.product_uom_qty  # Gán giá trị thực tế
            else:
                line.qty_delivered = 0  # Ẩn giá trị khi chưa có phiếu xuất kho
    #
    @api.depends('order_id.state')
    def _compute_qty_invoiced(self):
        for line in self:
            if line.order_id.state == 'sale':
                line.qty_invoiced = line.qty_delivered  # Hoặc giá trị khác tùy theo logic của bạn
            else:
                line.qty_invoiced = 0  # Ẩn giá trị khi chưa xác nhận đơn hàng

    #
    @api.depends('product_id', 'pricelist_id', 'order_id.state')
    def _compute_price_unit(self):
        for line in self:
            if line.product_id and line.pricelist_id:
                pricelist_item = line.pricelist_id.item_ids.filtered(lambda i: i.product_tmpl_id == line.product_id.product_tmpl_id)
                
                if pricelist_item:
                    if pricelist_item.compute_price == 'fixed':
                        line.price_unit = pricelist_item.fixed_price
                    elif pricelist_item.compute_price == 'formula' and pricelist_item.base_pricelist_id:
                        base_price = pricelist_item.base_pricelist_id.get_product_price(line.product_id, line.product_uom_qty, line.order_id.partner_id)
                        line.price_unit = base_price * (1 + pricelist_item.percent_price / 100)
                else:
                    line.price_unit = line.product_id.list_price  # Giá mặc định nếu không có bảng giá

    @api.onchange('product_id', 'pricelist_id')
    def _onchange_product_id(self):
        if self.product_id:
            self._compute_price_unit()

    def write(self, values):
        """ Không cho phép chỉnh sửa đơn giá khi đơn hàng đã xác nhận """
        if 'price_unit' in values:
            for line in self:
                if line.order_id.state in ['sale', 'done']:
                    raise ValueError("Không thể chỉnh sửa Đơn giá khi Đơn hàng đã xác nhận.")
        return super().write(values)



    @api.depends('product_uom_qty', 'price_unit', 'percent_hmv', 'percent_dealer', 'discount')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.product_uom_qty * (line.price_unit - line.price_unit * line.percent_hmv / 100 - line.price_unit * line.percent_dealer/100) - line.discount

    @api.depends('price_subtotal')
    def _compute_untaxed_amount(self):
        for line in self:
            line.untaxed_amount = line.price_subtotal

    @api.depends('price_subtotal', 'tax_id')
    def _compute_taxes(self):
        for line in self:
            tax_rate = sum(line.tax_id.mapped('amount')) / 100.0
            line.taxes = line.price_subtotal * tax_rate

    @api.depends('untaxed_amount', 'taxes')
    def _compute_total(self):
        for line in self:
            line.total = line.untaxed_amount + line.taxes

    @api.onchange('product_id')
    def _onchange_uom_product_id(self):
        if self.product_id and self.product_id.uom_id:
            self.product_uom = self.product_id.uom_id


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Nếu chưa có, bạn có thể định nghĩa lại các trường này hoặc ghi đè công thức tính của chúng.
    amount_untaxed = fields.Monetary(
        string="Untaxed Amount", 
        compute="_compute_amounts", 
        store=True, 
        currency_field='currency_id'
    )
    amount_tax = fields.Monetary(
        string="Taxes", 
        compute="_compute_amounts", 
        store=True, 
        currency_field='currency_id'
    )
    amount_total = fields.Monetary(
        string="Total", 
        compute="_compute_amounts", 
        store=True, 
        currency_field='currency_id'
    )

    @api.depends('order_line.price_subtotal', 'order_line.taxes')
    def _compute_amounts(self):
        for order in self:
            total_untaxed = sum(line.price_subtotal for line in order.order_line)
            total_tax = sum(line.taxes for line in order.order_line)
            order.amount_untaxed = total_untaxed
            order.amount_tax = total_tax
            order.amount_total = total_untaxed + total_tax            
