from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # x_identity_number = fields.Char(  # Đổi từ identity_number thành x_identity_number
    #     string='CCCD/CMT',
    #     help="Số Căn cước công dân hoặc Chứng minh thư",
    #     tracking=True
    # )
    x_fax = fields.Char(
        string='Fax',
        help="Số fax của đối tác",
        tracking=True  # Thêm tracking để theo dõi thay đổi
    )

    x_vehicle_ownership_date = fields.Datetime(  # Đổi từ Datetime sang Date vì chỉ cần ngày
        string='Ngày sở hữu xe',
        help="Ngày sở hữu xe của đối tác",
        tracking=True
    )

    x_business = fields.Selection([  # Đổi từ Char sang Selection để chuẩn hóa dữ liệu
        ('manufacturing', 'Sản xuất'),
        ('trading', 'Thương mại'),
        ('service', 'Dịch vụ'),
        ('transportation', 'Vận tải'),
        ('construction', 'Xây dựng'),
        ('other', 'Khác')
    ], string="Lĩnh vực hoạt động",
        help="Lĩnh vực hoạt động chính của đối tác",
        tracking=True
    )

    @api.constrains('x_fax')
    def _check_fax_format(self):
        """Kiểm tra định dạng số fax"""
        for record in self:
            if record.x_fax and not record.x_fax.replace('.', '').replace('-', '').isdigit():
                raise ValidationError(_('Số fax chỉ được chứa số và các ký tự . -'))

    @api.onchange('x_vehicle_ownership_date')
    def _onchange_ownership_date(self):
        """Kiểm tra ngày sở hữu xe không được lớn hơn ngày hiện tại"""
        if self.x_vehicle_ownership_date and self.x_vehicle_ownership_date > fields.Datetime.today():
            raise ValidationError(_('Ngày sở hữu xe không được lớn hơn ngày hiện tại'))
