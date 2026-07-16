from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    insider_ticket_ids = fields.One2many("insider.ticket", "partner_id")

    insider_ticket_count = fields.Integer(compute="_compute_insider_ticket_count")

    insider_open_late_count = fields.Integer(compute="_compute_insider_open_late_count")

    def _compute_insider_ticket_count(self):
        Ticket = self.env["insider.ticket"]
        ticket_grouped = Ticket._read_group(
            [
                ("partner_id", "in", self.ids),
            ],
            ["partner_id"],
            ['__count']
        )
        n_of_tickets_by_contact = dict(ticket_grouped)
        for partner in self:
            partner.insider_ticket_count = n_of_tickets_by_contact.get(partner, 0)

    def _compute_insider_open_late_count(self):
        Ticket = self.env["insider.ticket"]
        ticket_grouped = Ticket._read_group(
            [
                ("partner_id", "in", self.ids),
                ("is_late", "=", True),
                ("state", "!=", "done"),
            ],
            ["partner_id"],
            ['__count']
        )
        n_of_tickets_by_contact = {
            partner:count_tickets
            for (partner, count_tickets)
            in ticket_grouped
        }
        for partner in self:
            partner.insider_open_late_count = n_of_tickets_by_contact.get(partner, 0)