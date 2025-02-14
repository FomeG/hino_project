from odoo import models, fields, api

class ElectronicInvoice(models.Model):
    _inherit = 'sale.order'  # Kế thừa hóa đơn (invoice) trong Odoo

    x_electronic_invoice = fields.Boolean(
        string="Electronic Invoice",
        help="Allow selection to issue an electronic invoice"
    )
    x_invoiced_company = fields.Char(
        string="Invoiced Company",
        help="Name of the company issuing the invoice",
    )
    x_invoice_address = fields.Char(
        string="Invoice Address",
        help="Invoice issuing address",
    )
    x_tax_code = fields.Char(
        string="Tax Code",
        help="Tax identification number for invoicing",
    )
    x_buyer = fields.Char(
        string="Buyer",
        help="Purchaser's name",
    )
    x_email_received_invoice = fields.Char(
        string="Email Received Invoice",
        help="Email address for receiving the invoice",
    )