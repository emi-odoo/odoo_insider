from odoo import api, models, fields


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Product Brand"

    display_name = fields.Char(string="Display Name", compute="_compute_display_name")

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    partner_ids = fields.Many2many("res.partner")

    date = fields.Date()
    state = fields.Selection(
        [
            ("active", "Active"),
            ("closed", "Closed"),
            ("new", "New"),
        ]
    )

    @api.depends("name", "date")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} ({record.date})"
