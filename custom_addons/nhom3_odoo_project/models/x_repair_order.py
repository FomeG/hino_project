from odoo import models, fields, api
from odoo.exceptions import ValidationError
class ChuXe(models.Model):
    _inherit = 'repair.order'

 # Override name field to make it required and readonly
    name = fields.Char('Repair Reference', required=True, readonly=True, default='/')

    # Repair Type
    x_repair_type = fields.Selection([
        ('warranty', 'Warranty repairs'),
        ('free_maintenance', 'Free maintenance'),
        ('normal_maintenance', 'Normal maintenance'), 
        ('free_inspection', 'Free inspection'),
        ('spare_part', 'Spare part sales'),
        ('pdi', 'PDI')
    ], string='Repair Type', required=True)

    # Appointment
    x_schedule_id = fields.Many2one('calendar.event', string='Appointment')

    # CPUS Status 
    x_cpus_status = fields.Selection([
        ('cpus', 'CPUS'),
        ('non_cpus', 'Non CPUS')
    ], string='CPUS Status')

    # Repair Action
    x_repair_action = fields.Selection([
        ('new', 'New Repair'),
        ('redo', 'Redo Repair')
    ], string='Repair Action')

    # Repair Result
    x_repair_result = fields.Selection([
        ('pass', 'Pass'),
        ('pass_with_warning', 'Pass with Warning'),
        ('fail', 'Fail')
    ], string='Result')

    # Service Advisor
    x_service_advisor_id = fields.Many2one('res.users', string='Service Advisor', 
        default=lambda self: self.env.user)

    # Times
    x_entry_time = fields.Datetime('Entry Time')
    x_reception_time = fields.Datetime('Reception Time')
    x_expected_completion_time = fields.Datetime('Expected Completion Time')
    x_completion_time = fields.Datetime('Completion Time', readonly=True)

    # KM at repair
    x_km_at_repair = fields.Float('KM at Repair')

    # Execution Location
    x_execution_location = fields.Selection([
        ('outside', 'Outside Station'),
        ('inside', 'Inside Station')
    ], string='Execution Location', default='inside')

    @api.model
    def create(self, vals):
        return super(ChuXe, self).create(vals)

    def write(self, vals):
        if vals.get('state') == 'done':
            vals['x_completion_time'] = fields.Datetime.now()
            if not (self.x_cpus_status and self.x_repair_action and self.x_repair_result):
                raise ValidationError(("CPUS Status, Repair Action and Repair Result are required to complete repair"))
        return super(ChuXe, self).write(vals)
    
    def action_checkout(self):
        repair_order_id = self.env['repair.order'].search([('name', '=', self.name)], limit=1).id

        return {
            "name": "Payment request",
            'type': 'ir.actions.act_window',  # Ensure this is 'ir.actions.act_window' and not 'ir.action.act_window'
            'view_mode': 'form',
            'res_model': 'warranty.request',
            'view_id': self.env.ref('nhom3_odoo_project.view_warranty_request_form').id,
            'target': 'self',
            'context': {
                'create': False,
                'default_x_repair_order': repair_order_id,  # Truyền ID của repair.order vào context
            },
        }

    x_vehicle_plate = fields.Many2one('vehicle.information', string="License Plate")
    partner_id = fields.Many2one('res.partner', string="Vehicle Owner", compute="_compute_vehicle_owner", store=True)
    x_driver = fields.Char(string="Driver")
    x_driver_phone = fields.Char(string="Driver Phone")


    @api.depends('x_vehicle_plate')
    def _compute_vehicle_owner(self):
        """Tự động lấy chủ xe từ biển số"""
        for record in self:
            if record.x_vehicle_plate:
                record.partner_id = record.x_vehicle_plate.owner_info.id
            else:
                record.partner_id = False

    @api.onchange('x_vehicle_plate')
    def _onchange_vehicle_plate(self):
        """Tự động lấy thông tin lái xe và số điện thoại khi chọn biển số"""
        if self.x_vehicle_plate:
            self.partner_id = self.x_vehicle_plate.owner_info.id
            self.x_driver = self.x_vehicle_plate.driver.name if self.x_vehicle_plate.driver else ''
            self.x_driver_phone = self.x_vehicle_plate.driver_phone if self.x_vehicle_plate.driver_phone else ''

#Thông tin chung

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

    # Vehicle Information
    x_vehicle_plate = fields.Many2one('vehicle.information', string='License Plate', help='Vehicle license plate from vehicle information')
    x_vehicle_type = fields.Selection([
        ('hino', 'Hino'),
        # Add other types as needed
    ], string='Vehicle Type', default='hino')
    
    x_trademark = fields.Many2one('fleet.vehicle.model.brand', string='Brand', help='Vehicle brand from vehicle information', related='x_vehicle_plate.series_id')
    
    x_vehicle_model = fields.Many2one('fleet.vehicle.model', string='Model', help='Vehicle model from vehicle information', related='x_vehicle_plate.model_list_id')
    x_vin_number = fields.Char(string='VIN Number', help='VIN number from vehicle information', related='x_vehicle_plate.vin')
    
    x_engine_number = fields.Char(string='Engine Number', help='Engine number from vehicle information', related='x_vehicle_plate.engine_number')
    
    x_hmv_maintenance_expiry = fields.Date(string='HMV Maintenance Expiry Date', help='Expiry date from warranty registration')
    
    x_warranty_expiry = fields.Datetime(string='Warranty Expiry Date', help='Warranty expiry date from vehicle information', related='x_vehicle_plate.warranty_expire_date')


#list view
    x_quotation_id = fields.Char(string='Quotation Name')
    x_appointment_status = fields.Selection([
        ('draft', 'Unconfirmed'),
        ('open', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Appointment Status", default='draft')
    x_status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('repairing', 'Repairing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('created', 'Created'),
    ], string='Satus', default='draft',
        help="* The \'New\' status is used when a user is encoding a new and unconfirmed repair order.\n"
             "* The \'Confirmed\' status is used when a user confirms the repair order.\n"
             "* The \'Under Repair\' status is used when the repair is ongoing.\n"
             "* The \'Repaired\' status is set when repairing is completed.\n"
             "* The \'Cancelled\' status is used when user cancel repair order."
    )

    def button_repair_confirm(self):
        self.x_status = 'confirmed'

    def button_repair_start(self):
        self.x_status = 'repairing'

    def button_repair_end(self):
        self.x_status = 'completed'

    def _prepare_sale_order_values(self):
        """Chuẩn bị giá trị cho việc tạo báo giá từ lệnh sửa chữa"""
        self.ensure_one()

        # Xác định loại báo giá dựa trên loại sửa chữa
        repair_type_mapping = {
            'warranty': 'warranty',  # Warranty repairs -> Warranty
            'free_maintenance': 'maintenance',  # Free maintenance -> Maintenance
            'normal_maintenance': 'maintenance',  # Normal maintenance -> Maintenance
            'free_inspection': 'maintenance',  # Free inspection -> Maintenance
            'spare_part': 'spare_part',  # Spare part sales -> Spare_Parts
            'pdi': 'pdi'  # PDI -> Service
        }
        quote_type = repair_type_mapping.get(self.x_repair_type)

        # Chuẩn bị các giá trị cho báo giá
        values = {
            'partner_id': self.partner_id.id,
            'x_type_of_document': 'repair',
            'x_type_of_repair_order': quote_type,
            'pricelist_id': self.x_pricelist_id.id if self.x_pricelist_id else self.partner_id.property_product_pricelist.id,
            'origin': self.id,
            'date_order': fields.Datetime.now(),
        }

        return values

    def button_create_sale_order(self):
        self.x_status = 'created'

        """Tạo báo giá mới từ lệnh sửa chữa"""
        self.ensure_one()

        if not self.partner_id:
            raise ValidationError('Vui lòng chọn khách hàng trước khi tạo báo giá!')

        existing_sale_order = self.env['sale.order'].search([('origin', '=', self.name)], limit=1)

        if existing_sale_order:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Báo giá',
                'res_model': 'sale.order',
                'view_mode': 'form',
                'view_id': self.env.ref('nhom3_odoo_project.view_sale_order_form').id,
                'res_id': existing_sale_order.id,
                'target': 'current',
            }

        sale_order_values = self._prepare_sale_order_values()
        sale_order = self.env['sale.order'].create(sale_order_values)
        sale_order._onchange_partner_id()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Báo giá',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'view_id': self.env.ref('nhom3_odoo_project.view_sale_order_form').id,
            'res_id': sale_order.id,
            'target': 'current',
        }

    def button_repair_cancel(self):
        self.x_status = 'canceled'

    def button_repair_cancel_draft(self):
        self.x_status = 'draft'
