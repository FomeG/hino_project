# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WarrantyRequest(models.Model):
    _name = 'warranty.request'
    _description = 'Warranty Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    x_warranty_request_number = fields.Char(
        string='Warranty Request Number',
        required=True,
        help="Số YCTT bảo hành"
    )

    x_repair_order = fields.Many2one(
        'repair.order',
        string='Repair Order',
        help="Phiếu sửa chữa"
    )

    # Các trường lấy từ Repair Order
    x_plate_number = fields.Char(
        related='x_repair_order.x_vehicle_plate.name', 
        string="Plate Number", 
        readonly=True
    )
    vin = fields.Char(related='x_repair_order.x_vin_number', string="VIN", readonly=True)
    x_engine = fields.Char(related='x_repair_order.x_engine_number', string="Engine", readonly=True)
    x_warranty_expiry_date = fields.Datetime(
        related='x_repair_order.x_warranty_expiry', 
        string="Warranty Expiry Date", 
        readonly=True
    )

    x_owner_name=fields.Char(related='x_repair_order.partner_id.name',string="Owner vehicle name", readonly=True)
    x_address=fields.Char(related='x_repair_order.partner_id.street',string="Address", readonly=True)
    x_tel=fields.Char(related='x_repair_order.x_driver_phone',string="Phone", readonly=True)
    x_driver=fields.Char(related='x_repair_order.x_driver',string="Driver", readonly=True)
    x_driver_phone=fields.Char(related='x_repair_order.x_driver_phone',string="Phone", readonly=True)
    # x_total_requested_amount
    # x_total_approved_amount
    x_dealer_report_date = fields.Datetime(
        string='Dealer Report Date',
        help="Ngày đại lý báo hỏng"
    )

    x_owner_name = fields.Many2one(
        'res.partner',
        string='Owner Name',
        help="Tên chủ xe"
    )

    x_submission_count = fields.Float(
        string='Submission Count',
        help="Số lần đệ trình (đếm số lần ấn gửi phê duyệt tính trên 1 phiếu Yêu cầu thanh toán)"
    )

    x_dealer_opinion = fields.Char(
        string='Dealer Opinion',
        help="Ý kiến đại lý"
    )

    x_factory_opinion = fields.Char(
        string='Factory Opinion',
        help="Ý kiến nhà máy"
    )

    x_fault_report_title = fields.Char(
        string='Fault Report Title',
        help="Tiêu đề báo hỏng"
    )

    x_remaining_validity_days = fields.Float(
        string='Remaining Validity Days',
        help="Số ngày hiệu lực còn lại"
    )
    x_status = fields.Selection([
        ('draft', 'Draft'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    ], default='draft', string="Status")

        # Các field khác ...

    def action_send_approval(self):
        self.ensure_one()
        # Logic gửi duyệt
        self.x_status = 'in_progress'
        return True

    def action_cancel(self):
        self.ensure_one()
        # Logic hủy
        self.x_status = 'cancelled'
        return True

    def action_print(self):
        self.ensure_one()
        # Logic in phiếu
        return True

    def action_approve(self):
        self.ensure_one()
        # Logic duyệt
        self.x_status = 'approved'
        return True

    def action_reject(self):
        self.ensure_one()
        # Logic từ chối
        self.x_status = 'rejected'
        return True

    # 1. Số chứng từ
    x_number = fields.Char(string="Number", required=True)
    
    # 2. Phiếu sửa chữa BH (liên kết đến repair.order)
    x_repair_number = fields.Many2one(
        'repair.order',
        string="Repair Number",
        required=True,
    )

    
    # 3. Ngày từ ngày hoàn thành sửa chữa - tính theo công thức:
    #    Ngày hoàn thành của lệnh sửa chữa - Ngày đại lý tạo yêu cầu thanh toán
    # x_days_from_repair_completion = fields.Float(
    #     string="Days from repair completion",
    #     compute="_compute_days_from_repair_completion",
    #     store=True,
    #     required=True,
    #     help="Tính theo công thức = Ngày hoàn thành của lệnh sửa chữa – Ngày đại lý tạo yêu cầu thanh toán"
    # )
    
    # 4. Ngày tạo yêu cầu bảo hành
    x_warranty_request_date = fields.Datetime(string="Warranty Request Date", required=True)
    
    # 5. Ngày gửi yêu cầu bảo hành
    x_warranty_submission_date = fields.Datetime(string="Warranty Submission Date")
    
    # 6. Ngày xảy ra sự cố
    x_damaged_date = fields.Datetime(string="Damaged Date")
    
       # Các trường Many2one khác, ví dụ:
    x_hmv_check = fields.Many2one(
        'hmv.check', 
        string="HMV Check"
    )
    x_warranty_category = fields.Many2one(
        'warranty.category', 
        string="Warranty Category"
    )
    x_dealer_report = fields.Many2one(
        'dealer.report', 
        string="Dealer Report"
    )
    x_dealer_phone = fields.Many2one(
        'res.partner', 
        string="Dealer Phone", 
        ondelete='set null'
    )
    # 11. Điều kiện vận hành
    x_operation_conditions = fields.Char(string="Operation Conditions")
    
    # 12. Số lần hỏng tương tự lặp lại
    x_same_damaged_repeat = fields.Float(string="Same Damaged Repeat")
    
    # 13. Số km lúc hỏng
    x_km_damaged = fields.Float(string="Km Damaged")
    
    # 14. Số km thực tế (Ordometer reading)
    x_ordometer_reading = fields.Float(string="Ordometer Reading")
    
    # 15. Hiện tượng
    x_phenomenon = fields.Char(string="Phenomenon")
    
    # 16. Nguyên nhân hỏng
    x_causes_of_damaged = fields.Char(string="Causes of Damaged")
    
    # 17. Cải tạo/PT không chính hiệu
    x_not_genuine_spare_parts = fields.Char(string="Not Genuine Spare Parts")
    
    # 18. Ý kiến đại lý
    x_dealer_comment = fields.Char(string="Dealer Comment")
    
    # 19. Ý kiến của nhà máy
    x_factory_comment = fields.Char(string="Factory Comment")
    
    # 20. Biện pháp khắc phục
    x_remedies = fields.Char(string="Remedies")
    
    # 21. Công việc
    x_works = fields.Char(string="Works")
    
    # 22. Bộ phận hỏng
    x_damaged_part = fields.Char(string="Damaged Part")
    
    # 23. Bộ phận bị ảnh hưởng
    x_impact_part = fields.Char(string="Impact Part")
    
    # 24. Ý kiến khách hàng
    x_customer_comment = fields.Char(string="Customer Comment")
    
    # 25. Trả phụ tùng về nhà máy
    x_return_part_to_factory = fields.Char(string="Return Part to Factory")
    
    # 26. Lý do
    x_reason = fields.Char(string="Reason")

    @api.depends('x_repair_number.date_done', 'x_warranty_request_date')
    def _compute_days_from_repair_completion(self):
        for rec in self:
            if rec.x_repair_number and rec.x_repair_number.date_done and rec.x_warranty_request_date:
                delta = rec.x_repair_number.date_done - rec.x_warranty_request_date
                rec.x_days_from_repair_completion = delta.days
            else:
                rec.x_days_from_repair_completion = 0.0

class RepairOrder(models.Model):
    _name = 'repair.order'
    _inherit = 'repair.order'
    
    completion_date = fields.Datetime(string="Completion Date")
    date_done = fields.Datetime(string="Completion Date")
class DealerReport(models.Model):
    _name = 'dealer.report'
    _description = 'Dealer Report'

    name = fields.Char(string="Report Name", required=True)
class HMVCheck(models.Model):
    _name = 'hmv.check'  # Tên model
    _description = 'HMV Check'

    name = fields.Char(string="Check Name", required=True)
    date = fields.Date(string="Check Date", default=fields.Date.today)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='pending')

class WarrantyCategory(models.Model):
    _name = 'warranty.category'
    _description = 'Warranty Category'

    name = fields.Char(string="Name", required=True)
