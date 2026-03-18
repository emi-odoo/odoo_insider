from odoo import api, models, fields
from datetime import date

from odoo.exceptions import UserError

class ProductBrand(models.Model):
    _name = "product.brand"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    _description = "Product Brand"

    company_id = fields.Many2one("res.company")

    display_name = fields.Char(string="Display Name", compute="_compute_display_name")

    name = fields.Char(string="Name", required=True, translate=True)
    description = fields.Text(string="Description")
    partner_ids = fields.Many2many("res.partner")

    owner_id = fields.Many2one("res.partner")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    other_salesperson_id = fields.Many2one("res.users", string="Other Salesperson")

    my_field = fields.Integer(compute="_compute_my_field", store=True)
    m2o_field_id = fields.Many2one("res.partner")

    my_field = fields.Float()

    @api.depends("m2o_field_id")
    def _compute_my_field(self):
        for record in self:
            record.my_field = record.m2o_field_id.id if record.m2o_field_id else 0

    @api.onchange("name")
    def _onchange_name(self):
        self.description = self.name
        return {
            "warning": {
                "title": "you changed the name of the brand! beare",
                "message": "changing the name might have unforeseen consequence",
            }
        }

    date = fields.Date()
    state = fields.Selection(
        [
            ("active", "Active"),
            ("closed", "Closed"),
            ("new", "New"),
        ]
    )
    _name_uniq = models.UniqueIndex("(name)", "Name already exists")
    _state_idx = models.Index("(name, state) WHERE state = 'active'")

    @api.depends("name", "date")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} ({record.date})"

    def move_close_if_old_enough(self):
        self.ensure_one()
        if (date.today() - self.date).days > 200:
            self.state = "closed"
        else:
            raise UserError("This brand is not old enough to be closed")
