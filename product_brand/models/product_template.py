from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    brand_ids = fields.Many2many("product.brand", string="Brands")
    brand_id = fields.Many2one("product.brand", string="Brand")
