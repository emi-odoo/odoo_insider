from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _my_method(self):
        self.ensure_one()
        return self.name
