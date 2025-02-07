from odoo import fields, models, api
from odoo.exceptions import ValidationError
class SmartButtons(models.Model):
    _inherit = 'repair.order'

    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count")

    # Contact smart button
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['calendar.event'].search_count([('id', '=', record.x_schedule_id.id)])

    def action_contact(self):
        return {
            'name': 'Contact',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'calendar.event',
            'domain': [('id', '=', self.x_schedule_id.id)],
            'context': {'create': False},
        }

    def _prepare_sale_order_values(self):
        """Chuẩn bị giá trị cho việc tạo báo giá từ lệnh sửa chữa"""
        self.ensure_one()

        # Logic ánh xạ từ repair_type sang type_of_repair_order
        repair_type_mapping = {
            'warranty': 'warranty',  # Bảo hành
            'free_maintenance': 'maintenance',  # Bảo dưỡng miễn phí
            'normal_maintenance': 'maintenance',  # Bảo dưỡng định kỳ
            'free_inspection': 'maintenance',  # Kiểm tra miễn phí
            'spare_part': 'parts',  # Bán phụ tùng
            'pdi': 'service'  # PDI
        }

        # Kiểm tra và lấy pricelist phù hợp
        pricelist = self.x_pricelist_id
        if not pricelist and self.partner_id:
            # Tìm bảng giá được áp dụng cho khách hàng
            domain = [
                ('partner_ids', 'in', self.partner_id.id),
                '|', ('date_start', '<=', fields.Date.today()), ('date_start', '=', False),
                '|', ('date_end', '>=', fields.Date.today()), ('date_end', '=', False)
            ]
            pricelist = self.env['product.pricelist'].search(domain, limit=1)
            if not pricelist:
                # Nếu không tìm thấy, sử dụng bảng giá mặc định của khách hàng
                pricelist = self.partner_id.property_product_pricelist

        # Chuẩn bị các giá trị cho báo giá
        values = {
            'partner_id': self.partner_id.id,
            'x_type_of_document': 'repair',  # Loại chứng từ là từ lệnh sửa chữa
            'x_type_of_repair_order': repair_type_mapping.get(self.x_repair_type, 'service'),
            'pricelist_id': pricelist.id,
            'origin': self.id,
            'date_order': fields.Datetime.now(),
            # Thêm các trường khác nếu cần
            'x_vehicle_plate': self.x_vehicle_plate.id if hasattr(self, 'x_vehicle_plate') else False,
            'user_id': self.x_service_advisor_id.id if hasattr(self, 'x_service_advisor_id') else self.env.user.id,
        }

        return values

    # Order quotations smart button
    def action_order_quotations(self):
        """Tạo báo giá mới từ lệnh sửa chữa"""
        self.ensure_one()

        # Kiểm tra điều kiện trước khi tạo
        if not self.partner_id:
            raise ValidationError('Vui lòng chọn khách hàng trước khi tạo báo giá!')

        # Chuẩn bị giá trị cho báo giá
        sale_order_values = self._prepare_sale_order_values()

        # Tạo báo giá mới
        sale_order = self.env['sale.order'].create(sale_order_values)

        # Cập nhật thông tin địa chỉ từ partner
        sale_order._onchange_partner_id()

        # Trả về action để mở báo giá vừa tạo
        return {
            'type': 'ir.actions.act_window',
            'name': _('Báo giá'),
            'res_model': 'sale.order',
            'res_id': 'view_sale_order_form',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }

    # Export inventory smart button
    def action_export_inv(self):
        return

    # Customer care smart button
    def action_customer_care(self):
        return

    # Customer complaint smart button
    def action_complaint(self):
        return

    def action_checkout(self):
        return

