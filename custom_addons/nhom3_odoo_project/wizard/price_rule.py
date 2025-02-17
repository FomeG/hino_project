# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Price_Rule_Wizard(models.Model):
    _inherit = 'product.pricelist'

    def action_data_import(self):
        """Open the price rule wizard"""
        return {
            'name': _('Import Price Rule'),
            'type': 'ir.actions.act_window',
            'res_model': 'price.rule.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_pricelist_id': self.id,
                'default_currency_id': self.currency_id.id,
                'default_company_id': self.company_id.id,
            }
        }