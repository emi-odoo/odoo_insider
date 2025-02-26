from odoo import api, models


class SaleOrder(models.AbstractModel):
    _name = "report.sale.report_saleorder"

    @api.model
    def _get_report_values(self, doc_ids, data=None):
        lines = []

        return {
            "doc_ids": doc_ids,
            "doc_model": self.env["sale.order"],
            "data": data,
            "docs": self.env["sale.order"].browse(doc_ids),
            "new_variable": "Hello World",
        }
