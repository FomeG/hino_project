from odoo import models, fields, api
INVOICE_STATUS = [
    ('upselling', 'Upselling Opportunity'),
    ('invoiced', 'Fully Invoiced'),
    ('to invoice', 'To Invoice'),
    ('no', 'Nothing to Invoice')
]
class ElectronicInvoice(models.Model):
    _inherit = 'sale.order'

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
      # tab other info
    user_id = fields.Many2one('res.users', string='User')
    team_id = fields.Many2one('crm.team', string='Team')
    company_id = fields.Many2one('res.company', string='Company')
    require_signature = fields.Boolean(string='Online Signature')
    require_payment = fields.Boolean(string='Online Payment')
    client_order_ref = fields.Char(string='Client Order Ref')
    tag_ids = fields.Many2many('crm.tag', string='Tags')

    incoterm = fields.Many2one('account.incoterms', string='Incoterm')
    incoterm_location = fields.Char(string='Incoterm Location')
    picking_policy = fields.Selection([
        ('direct', 'As soon as possible'),
        ('one', 'When all products are ready')],
        string='Shipping Policy', required=True, default='direct',
        help="If you deliver all products at once, the delivery order will be scheduled based on the greatest "
             "product lead time. Otherwise, it will be based on the shortest.")

    shipping_weight = fields.Float("Shipping Weight", compute="_compute_shipping_weight", store=True, readonly=False)
    commitment_date = fields.Datetime(
        string="Delivery Date", copy=False,
        help="This is the delivery date promised to the customer. "
             "If set, the delivery order will be scheduled based on "
             "this date rather than product lead times.")
    effective_date = fields.Datetime("Effective Date", compute='_compute_effective_date', store=True,
                                     help="Completion date of the first delivery order.")
    delivery_status = fields.Selection([
        ('pending', 'Not Delivered'),
        ('started', 'Started'),
        ('partial', 'Partially Delivered'),
        ('full', 'Fully Delivered'),
    ], string='Delivery Status', compute='_compute_delivery_status', store=True)

    fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position',
        string="Fiscal Position",
        compute='_compute_fiscal_position_id',
        store=True, readonly=False, precompute=True, check_company=True,
        help="Fiscal positions are used to adapt taxes and accounts for particular customers or sales orders/invoices."
             "The default value comes from the customer.",
    )
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string="Analytic Account",
        copy=False, check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    journal_id = fields.Many2one(
        'account.journal', string="Invoicing Journal",
        compute="_compute_journal_id", store=True, readonly=False, precompute=True,
        domain=[('type', '=', 'sale')], check_company=True,
        help="If set, the SO will invoice in this journal; "
             "otherwise the sales journal with the lowest sequence is used.")
    invoice_status = fields.Selection(
        selection=INVOICE_STATUS,
        string="Invoice Status",
        compute='_compute_invoice_status',
        store=True)

    origin1 = fields.Char(
        string="Source Document",
        help="Reference of the document that generated this sales order request")
    campaign_id = fields.Many2one(ondelete='set null')
    medium_id = fields.Many2one(ondelete='set null')
    source_id = fields.Many2one(ondelete='set null')

    # @api.depends('order_line.product_uom_qty', 'order_line.product_uom')
    # def _compute_shipping_weight(self):
    #     for order in self:
    #         order.shipping_weight = order._get_estimated_weight()
    #
    # @api.depends('picking_ids.date_done')
    # def _compute_effective_date(self):
    #     for order in self:
    #         pickings = order.picking_ids.filtered(
    #             lambda x: x.state == 'done' and x.location_dest_id.usage == 'customer')
    #         dates_list = [date for date in pickings.mapped('date_done') if date]
    #         order.effective_date = min(dates_list, default=False)
    #
    # @api.depends('picking_ids', 'picking_ids.state')
    # def _compute_delivery_status(self):
    #     for order in self:
    #         if not order.picking_ids or all(p.state == 'cancel' for p in order.picking_ids):
    #             order.delivery_status = False
    #         elif all(p.state in ['done', 'cancel'] for p in order.picking_ids):
    #             order.delivery_status = 'full'
    #         elif any(p.state == 'done' for p in order.picking_ids) and any(
    #                 l.qty_delivered for l in order.order_line):
    #             order.delivery_status = 'partial'
    #         elif any(p.state == 'done' for p in order.picking_ids):
    #             order.delivery_status = 'started'
    #         else:
    #             order.delivery_status = 'pending'
    #
    # @api.depends('partner_shipping_id', 'partner_id', 'company_id')
    # def _compute_fiscal_position_id(self):
    #     """
    #     Trigger the change of fiscal position when the shipping address is modified.
    #     """
    #     cache = {}
    #     for order in self:
    #         if not order.partner_id:
    #             order.fiscal_position_id = False
    #             continue
    #         fpos_id_before = order.fiscal_position_id.id
    #         key = (order.company_id.id, order.partner_id.id, order.partner_shipping_id.id)
    #         if key not in cache:
    #             cache[key] = self.env['account.fiscal.position'].with_company(
    #                 order.company_id
    #             )._get_fiscal_position(order.partner_id, order.partner_shipping_id).id
    #         if fpos_id_before != cache[key] and order.order_line:
    #             order.show_update_fpos = True
    #         order.fiscal_position_id = cache[key]
    #
    # def _compute_journal_id(self):
    #     self.journal_id = False
    #
    # @api.depends('state', 'order_line.invoice_status')
    # def _compute_invoice_status(self):
    #     """
    #     Compute the invoice status of a SO. Possible statuses:
    #     - no: if the SO is not in status 'sale' or 'done', we consider that there is nothing to
    #       invoice. This is also the default value if the conditions of no other status is met.
    #     - to invoice: if any SO line is 'to invoice', the whole SO is 'to invoice'
    #     - invoiced: if all SO lines are invoiced, the SO is invoiced.
    #     - upselling: if all SO lines are invoiced or upselling, the status is upselling.
    #     """
    #     confirmed_orders = self.filtered(lambda so: so.state == 'sale')
    #     (self - confirmed_orders).invoice_status = 'no'
    #     if not confirmed_orders:
    #         return
    #     lines_domain = [('is_downpayment', '=', False), ('display_type', '=', False)]
    #     line_invoice_status_all = [
    #         (order.id, invoice_status)
    #         for order, invoice_status in self.env['sale.order.line']._read_group(
    #             lines_domain + [('order_id', 'in', confirmed_orders.ids)],
    #             ['order_id', 'invoice_status']
    #         )
    #     ]
    #     for order in confirmed_orders:
    #         line_invoice_status = [d[1] for d in line_invoice_status_all if d[0] == order.id]
    #         if order.state != 'sale':
    #             order.invoice_status = 'no'
    #         elif any(invoice_status == 'to invoice' for invoice_status in line_invoice_status):
    #             if any(invoice_status == 'no' for invoice_status in line_invoice_status):
    #                 # If only discount/delivery/promotion lines can be invoiced, the SO should not
    #                 # be invoiceable.
    #                 invoiceable_domain = lines_domain + [('invoice_status', '=', 'to invoice')]
    #                 invoiceable_lines = order.order_line.filtered_domain(invoiceable_domain)
    #                 special_lines = invoiceable_lines.filtered(
    #                     lambda sol: not sol._can_be_invoiced_alone()
    #                 )
    #                 if invoiceable_lines == special_lines:
    #                     order.invoice_status = 'no'
    #                 else:
    #                     order.invoice_status = 'to invoice'
    #             else:
    #                 order.invoice_status = 'to invoice'
    #         elif line_invoice_status and all(invoice_status == 'invoiced' for invoice_status in line_invoice_status):
    #             order.invoice_status = 'invoiced'
    #         elif line_invoice_status and all(
    #                 invoice_status in ('invoiced', 'upselling') for invoice_status in line_invoice_status):
    #             order.invoice_status = 'upselling'
    #         else:
    #             order.invoice_status = 'no'
