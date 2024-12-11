from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    longitude = fields.Float()
    latitude = fields.Float()
