from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class VehicleInformation(models.Model):
    _name = 'vehicle.information'
    _description = 'Vehicle Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Thông tin header chứng từ
    import_date = fields.Datetime(string='Ngày nhập khẩu', tracking=True)
    line_of_date = fields.Datetime(string='Ngày xuất xưởng', tracking=True)
    date_to_dealer = fields.Datetime(string='Ngày giao cho đại lý', tracking=True)
    company_id = fields.Many2one('res.company', string='Đại lý', required=True,
                                default=lambda self: self.env.company, tracking=True)
    original_id = fields.Many2one('res.partner', string='Nguồn',
                                 domain="[('is_company', '=', True)]", tracking=True)  # Sử dụng res.partner cho nhà cung cấp
    sales_order_id = fields.Many2one('sale.order', string='Đơn bán hàng', tracking=True,
                                    domain="[('company_id', '=', company_id)]")

    # Thông tin chung
    vin = fields.Char(string='Số khung', required=True, tracking=True)
    series_id = fields.Many2one('fleet.vehicle.model.brand', string='Dòng xe', tracking=True)  # Sử dụng model từ module fleet
    engine_number = fields.Char(string='Số máy', required=True, tracking=True)
    plate_number = fields.Char(string='Biển số', required=True, tracking=True)
    carbin_certificate_date = fields.Datetime(string='Carbin certificate date', tracking=True)
    carbin_certificate_number = fields.Char(string='Carbin certificate number', tracking=True)  # Đổi sang Char để lưu cả số và chữ
    body_type_id = fields.Selection([  # Thay thế bằng selection field
        ('truck', 'Xe tải'),
        ('bus', 'Xe khách'),
        ('trailer', 'Rơ moóc')
    ], string='Loại thùng', tracking=True)
    body_marker = fields.Char(string='Nơi làm thùng', tracking=True)
    front_axle = fields.Char(string='Trục trước', tracking=True)
    f_r_axle = fields.Char(string='Trục sau trước', tracking=True)
    rear_axle = fields.Char(string='Trục sau', tracking=True)
    lot = fields.Char(string='Lô', tracking=True)
    model_list_id = fields.Many2one('fleet.vehicle.model', string='Mẫu xe', tracking=True)  # Sử dụng model từ module fleet
    payload = fields.Float(string='Tải trọng (kg)', tracking=True)
    pdi_date = fields.Datetime(string='Ngày PDI', tracking=True)
    kms_at_pdi = fields.Float(string='Kms at PDI', tracking=True)
    key_number = fields.Char(string='Số chìa', tracking=True)
    color = fields.Char(string='Màu', tracking=True)  # Đổi từ Many2one sang Char
    cylinder_no = fields.Char(string='Xylanh', tracking=True)
    trans_number = fields.Char(string='Hộp số', tracking=True)
    f_r_diff = fields.Char(string='Vi sai trục S/T', tracking=True)
    rear_diff = fields.Char(string='Vi sai trục sau', tracking=True)
    battery_1 = fields.Char(string='Ắc quy 1', tracking=True)
    battery_2 = fields.Char(string='Ắc quy 2', tracking=True)
    note = fields.Text(string='Ghi chú', tracking=True)

    # Thông tin bảo hành
    approved_warranty_reg = fields.Boolean(string='Duyệt đăng ký bảo hành', tracking=True)
    warranty_registrator = fields.Boolean(string='Đăng ký bảo hành', default=True, tracking=True)
    booklet_number = fields.Char(string='Số bảo hành', tracking=True)
    bdmp_to_km = fields.Float(string='BDMP đến km', tracking=True)
    dmmp_count = fields.Float(string='SL.Phiếu DNMP', tracking=True)
    warranty_register_date = fields.Datetime(string='Ngày đăng ký bảo hành', tracking=True)
    warranty_expire_date = fields.Datetime(string='Ngày hết hạn bảo hành', tracking=True)
    odometer_reading = fields.Float(string='Km lúc bàn giao xe', tracking=True)
    customer_delivery_date = fields.Datetime(string='Ngày giao xe cho khách hàng', tracking=True)
    warranty_note = fields.Text(string='Ghi chú bảo hành', tracking=True)

    # Thông tin khách hàng
    owner_info = fields.Many2one('res.partner', string='Thông tin chủ xe', tracking=True)
    owner_name = fields.Char(related='owner_info.name', string='Chủ sở hữu', tracking=True)
    address = fields.Char(related='owner_info.street', string='Địa chỉ', tracking=True)
    identification_number = fields.Char(related='owner_info.ref',
                                       string='Số CMT/CCCD', tracking=True)  # Sử dụng field chuẩn cho số ID
    tax_code = fields.Char(related='owner_info.vat', string='Mã số thuế', tracking=True)
    contact_phone = fields.Char(related='owner_info.mobile', string='Điện thoại của chủ sở hữu', tracking=True)
    driver = fields.Many2one('res.partner', string='Lái xe', tracking=True)
    driver_phone = fields.Char(related='driver.mobile', string='Điện thoại lái xe', tracking=True)
    fax = fields.Char(related='owner_info.x_fax', string='Fax', tracking=True)
    contact = fields.Many2one('res.partner', string='Người liên hệ', tracking=True)
    contact_phone_2 = fields.Char(related='contact.mobile', string='Điện thoại người liên hệ', tracking=True)
    vehicle_ownership_date = fields.Datetime(related='owner_info.x_vehicle_ownership_date',
                                             string='Ngày sở hữu xe', tracking=True)
    customer_type = fields.Selection(related='owner_info.company_type', string='Loại doanh nghiệp', tracking=True)
    business = fields.Selection(related='owner_info.x_business',  # Thêm lĩnh vực hoạt động
                                string='Lĩnh vực hoạt động', tracking=True)
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