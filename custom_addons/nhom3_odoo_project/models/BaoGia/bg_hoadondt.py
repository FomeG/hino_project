from odoo import models, fields, api

class ElectronicInvoice(models.Model):
    _inherit = 'sale.order'  # Kế thừa hóa đơn (invoice) trong Odoo

    x_electronic_invoice = fields.Boolean(
        string="Electronic Invoice",
        help="Cho phép tích chọn hoặc không để thực hiện xuất hoá đơn điện tử"
    )
    x_invoiced_company = fields.Char(
        string="Invoiced Company",
        help="Tên Công ty xuất HD",
    )
    x_invoice_address = fields.Char(
        string="Invoice Address",
        help="Địa chỉ xuất HĐ",
    )
    x_tax_code = fields.Char(
        string="Tax Code",
        help="Mã số thuế xuất HĐ",
    )
    x_buyer = fields.Char(
        string="Buyer",
        help="Người mua hàng",
    )
    x_email_received_invoice = fields.Char(
        string="Email Received Invoice",
        help="Email nhận HĐ",
    )