from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class VehicleInformation(models.Model):
    _name = 'vehicle.information'
    _description = 'Vehicle Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Thông tin header chứng từ
    import_date = fields.Datetime(string='Import date', tracking=True)
    line_of_date = fields.Datetime(string='Line of date', tracking=True)
    date_to_dealer = fields.Datetime(string='Date to dealer', tracking=True)
    company_id = fields.Many2one('res.company', string='Dealer', required=True,
                                default=lambda self: self.env.company, tracking=True)
    original_id = fields.Many2one('res.partner', string='Original',
                                 domain="[('is_company', '=', True)]", tracking=True)  # Sử dụng res.partner cho nhà cung cấp
    sales_order_id = fields.Many2one('sale.order', string='Sales Order', tracking=True,
                                    domain="[('company_id', '=', company_id)]")

    # Thông tin chung
    vin = fields.Char(string='VIN', required=True, tracking=True)
    series_id = fields.Many2one('fleet.vehicle.model.brand', string='Serie', tracking=True)  # Sử dụng model từ module fleet
    engine_number = fields.Char(string='Engine', required=True, tracking=True)
    name = fields.Char(string='Plate number', required=True, tracking=True)
    carbin_certificate_date = fields.Datetime(string='Carbin certificate date', tracking=True)
    carbin_certificate_number = fields.Char(string='Carbin certificate number', tracking=True)  # Đổi sang Char để lưu cả số và chữ
    body_type_id = fields.Selection([  # Thay thế bằng selection field
        ('truck', 'Xe tải'),
        ('bus', 'Xe khách'),
        ('trailer', 'Rơ moóc')
    ], string='Body type', tracking=True)
    body_marker = fields.Char(string='Body maker', tracking=True)
    front_axle = fields.Char(string='Front axle', tracking=True)
    f_r_axle = fields.Char(string='F/R axle', tracking=True)
    rear_axle = fields.Char(string='Rear axle', tracking=True)
    lot = fields.Char(string='Lot', tracking=True)
    model_list_id = fields.Many2one('fleet.vehicle.model', string='Model list', tracking=True)  # Sử dụng model từ module fleet
    payload = fields.Float(string='Payload (kg)', tracking=True)
    pdi_date = fields.Datetime(string='PDI date', tracking=True)
    kms_at_pdi = fields.Float(string='Kms at PDI', tracking=True)
    key_number = fields.Char(string='Key number', tracking=True)
    color = fields.Char(string='Color', tracking=True)  # Đổi từ Many2one sang Char
    cylinder_no = fields.Char(string='Cylinder no', tracking=True)
    trans_number = fields.Char(string='Trans number', tracking=True)
    f_r_diff = fields.Char(string='F/R diff', tracking=True)
    rear_diff = fields.Char(string='Rear diff', tracking=True)
    battery_1 = fields.Char(string='Battery 1', tracking=True)
    battery_2 = fields.Char(string='Battery 2', tracking=True)
    note = fields.Text(string='Note', tracking=True)

    # Thông tin bảo hành
    approved_warranty_reg = fields.Boolean(string='Approved warranty reg', tracking=True)
    warranty_registrator = fields.Boolean(string='Warranty registrator', default=True, tracking=True)
    booklet_number = fields.Char(string='Booklet number', tracking=True)
    bdmp_to_km = fields.Float(string='Free main to kms', tracking=True)
    dmmp_count = fields.Float(string='Lubricant coupons', tracking=True)
    warranty_register_date = fields.Datetime(string='Warranty register date', tracking=True)
    warranty_expire_date = fields.Datetime(string='Warranty expire date', tracking=True)
    odometer_reading = fields.Float(string='Odometer reading', tracking=True)
    customer_delivery_date = fields.Datetime(string='Customer Delivery Date', tracking=True)
    warranty_note = fields.Text(string='Note', tracking=True)

    # Thông tin khách hàng
    owner_info = fields.Many2one('res.partner', string='Owner infor', tracking=True)
    owner_name = fields.Char(related='owner_info.name', string='Owner name', tracking=True)
    address = fields.Char(related='owner_info.street', string='Address', tracking=True)
    identification_number = fields.Char(related='owner_info.ref',
                                       string='Personal ID', tracking=True)  # Sử dụng field chuẩn cho số ID
    tax_code = fields.Char(related='owner_info.vat', string='Tax code', tracking=True)
    contact_phone = fields.Char(related='owner_info.mobile', string='Phone of owner', tracking=True)
    driver = fields.Many2one('res.partner', string='Driver', tracking=True)
    driver_phone = fields.Char(related='driver.mobile', string='Phone of driver', tracking=True)
    fax = fields.Char(related='owner_info.x_fax', string='Fax', tracking=True)
    contact = fields.Many2one('res.partner', string='Contact', tracking=True)
    contact_phone_2 = fields.Char(related='contact.mobile', string='Phone of contact', tracking=True)
    vehicle_ownership_date = fields.Datetime(related='owner_info.x_vehicle_ownership_date',
                                             string='Vehicle ownership date', tracking=True)
    customer_type = fields.Selection(related='owner_info.company_type', string='Customer type', tracking=True)
    business = fields.Selection(related='owner_info.x_business',  # Thêm lĩnh vực hoạt động
                                string='Kind of Business', tracking=True)
    _sql_constraints = [
        ('vin_unique', 'unique(vin)', 'Số khung đã tồn tại!'),
        ('engine_number_unique', 'unique(engine_number)', 'Số máy đã tồn tại!'),
        ('plate_number_unique', 'unique(plate_number)', 'Biển số đã tồn tại!')
    ]

    @api.onchange('sales_order_id')
    def _onchange_sales_order(self):
        """Cập nhật thông tin khách hàng từ đơn hàng"""
        if self.sales_order_id:
            self.owner_info = self.sales_order_id.partner_id
            self.driver = self.sales_order_id.partner_id

    @api.constrains('vin', 'engine_number', 'plate_number')
    def _check_unique_identifiers(self):
        """Kiểm tra trùng lặp các định danh xe"""
        for record in self:
            if self.env['vehicle.information'].search_count([
                ('vin', '=', record.vin),
                ('id', '!=', record.id)
            ]) > 0:
                raise ValidationError(_('Số khung đã tồn tại!'))
            # Thêm các kiểm tra tương tự cho engine_number và plate_number

    def action_approve_warranty(self):
        """Phê duyệt bảo hành và tự động điền ngày hết hạn"""
        self.ensure_one()
        if not self.warranty_register_date:
            self.warranty_register_date = fields.Datetime.now()
        self.approved_warranty_reg = True
        self.warranty_expire_date = self.warranty_register_date + relativedelta(years=2)