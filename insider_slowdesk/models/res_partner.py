from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    insider_ticket_ids = fields.One2many("insider.ticket", "partner_id")

    # PERF BUG #2
    insider_ticket_count = fields.Integer(compute="_compute_insider_ticket_count")

    # PERF BUG #2b
    insider_open_late_count = fields.Integer(compute="_compute_insider_open_late_count")

    def _compute_insider_ticket_count(self):
        Ticket = self.env["insider.ticket"]
        for partner in self:
            partner.insider_ticket_count = len(
                Ticket.search([("partner_id", "=", partner.id)])
            )

    def _compute_insider_open_late_count(self):
        Ticket = self.env["insider.ticket"]
        for partner in self:
            tickets = Ticket.search([("partner_id", "=", partner.id)])
            partner.insider_open_late_count = len(
                [t for t in tickets if t.is_late and t.state != "done"]
            )
