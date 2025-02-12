# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_button_one(self):
        """
        Hàm này được gọi khi nhấn nút 'Button One'.
        Thông thường bạn sẽ xử lý logic tùy chỉnh ở đây.
        Ví dụ: hiển thị thông báo, cập nhật trạng thái,
        tạo bản ghi mới, v.v.
        """
        # Ví dụ minh họa: hiển thị một thông báo lỗi đơn giản
        raise UserError("Bạn vừa bấm 'Button One'!")

    def action_button_two(self):
        """
        Hàm này được gọi khi nhấn nút 'Button Two'.
        """
        # Ví dụ minh họa: ghi log
        # self.env['mail.message'].create(...)  # Hoặc dùng self.message_post(...)
        # Hoặc thực hiện thêm xử lý tùy ý
        raise UserError("Bạn vừa bấm 'Button Two'!")

    def action_button_three(self):
        """
        Hàm này được gọi khi nhấn nút 'Button Three'.
        """
        # Ví dụ minh họa: Tạo 1 record trong model khác, v.v.
        # new_record = self.env['some.model'].create({...})
        raise UserError("Bạn vừa bấm 'Button Three'!")
