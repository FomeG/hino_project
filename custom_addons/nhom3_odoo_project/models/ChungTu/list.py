from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ListView(models.Model):
    _inherit = 'repair.order'

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
