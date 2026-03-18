from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    _inherits = {"product.brand": "brand_id"}

    brand_id = fields.Many2one(
        "product.brand", string="Brand", required=True, ondelete="cascade"
    )
