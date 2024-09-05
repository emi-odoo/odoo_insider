from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    brand_id = fields.Many2one("product.brand")

    """
    SELECT
     sol.id,
     sol.name,
     --> t.brand_id
    FROM sale_order_line sol
    INNER JOIN product_template t
    ON sol.product_id = t.id

    GROUP BY
        sol.id,
        sol.name,
        --> t.brand_id
    """

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["brand_id"] = "t.brand_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            t.brand_id"""
        return res
