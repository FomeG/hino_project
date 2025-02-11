from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SmartButtons(models.Model):
    _inherit = 'repair.order'

    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count")
    repair_order_count = fields.Integer(string="Repair Order Count", compute="_compute_repair_order_count")

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

    # Order quotations smart button
    def _compute_repair_order_count(self):
        for record in self:
            record.repair_order_count = self.env['sale.order'].search_count([('x_appointment_id', '=', record.id)])

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
            'name': 'Báo giá',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'view_id': self.env.ref('nhom3_odoo_project.view_sale_order_form').id,
            'res_id': sale_order.id,
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
