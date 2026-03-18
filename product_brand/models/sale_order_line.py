from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_brand_id = fields.Many2one('product.brand', string='Product Brand', related='product_id.product_tmpl_id.brand_id', store=True)