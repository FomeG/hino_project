from odoo import api, fields, models

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    vehicle_id = fields.Many2one('fleet.vehicle', string='VIN Number', required=True)
    x_km_at_repair = fields.Float(string='KM at Repair', required=True)
    x_pricelist_id = fields.Many2one(
        'product.pricelist',
        string='Price List',
        compute='_compute_applicable_pricelist',
        store=True
    )

    @api.depends('partner_id', 'vehicle_id', 'x_km_at_repair')
    def _compute_applicable_pricelist(self):
        """
        Compute the applicable price list based on:
        - Customer (partner_id)
        - Vehicle (vehicle_id)
        - Current mileage (x_km_at_repair)
        """
        for record in self:
            # Search for applicable price lists
            pricelist = self.env['product.pricelist'].search([
                '|',
                ('applies_to_customer', '=', record.partner_id.id),
                '|',
                ('applies_to_vehicle', '=', record.vehicle_id.id),
                ('applies_to_km', '<=', record.x_km_at_repair)
            ], limit=1)

            record.x_pricelist_id = pricelist.id if pricelist else False

    @api.model
    def create(self, vals):
        """Override create to ensure pricelist is computed on creation"""
        res = super(RepairOrder, self).create(vals)
        res._compute_applicable_pricelist()
        return res

    def write(self, vals):
        """Override write to ensure pricelist is recomputed when relevant fields change"""
        res = super(RepairOrder, self).write(vals)
        if any(field in vals for field in ['partner_id', 'vehicle_id', 'x_km_at_repair']):
            self._compute_applicable_pricelist()
        return res