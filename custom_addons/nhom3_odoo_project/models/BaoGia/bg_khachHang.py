from odoo import models, fields
class baoGiaKhachHang(models.Model):
        _inherit='sale.order'
        
        name=fields.Char(string='Number',required=True)
        x_type_of_document=fields.Selection([
                ('ban_phu_tung','Bán phụ tùng'),
                ('don_lenh_sua_chua','Đơn lệnh sửa chữa')
        ],string='Type of document',default ='don_lenh_sua_chua',required=True)
        x_type_of_repair_order=fields.Selection([
                ('bao_hanh','Bảo hành'),
                ('bao_duong','Bảo dưỡng')
        ],string='Type of Repair Order')
        date_order=fields.datetime(string='Order Date',required=True)
        partner_id=fields.Many2one('res.partner',string='Customer',)