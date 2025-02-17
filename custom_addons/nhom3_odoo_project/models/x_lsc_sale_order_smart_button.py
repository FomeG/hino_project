# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    #Smart button
    def action_smart_button_delivery(self):
        raise UserError("Bạn vừa bấm 'Button action_smart_button_delivery ")

    def action_smart_button_create_invoice(self):
        raise UserError("Bạn vừa bấm 'Button action_smart_button_create_invoice'!")

    #Header button
    def action_button_delivery(self):
        raise UserError("Bạn vừa bấm 'Button action_button_delivery'!")

    def action_button_create_invoice(self):
        raise UserError("Bạn vừa bấm 'Button action_button_create_invoice'!")


    def action_button_cancel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'target': 'main'
        }
