import difflib
import logging
import random

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class InsiderTicketTag(models.Model):
    _name = "insider.ticket.tag"
    _description = "Ticket Tag"

    name = fields.Char(required=True)
    color = fields.Integer()


class InsiderTicket(models.Model):
    _name = "insider.ticket"
    _description = "Support Ticket (deliberately slow)"
    _order = "create_date desc"

    name = fields.Char(required=True)

    # PERF BUG #3a
    reference = fields.Char(readonly=True, copy=False)

    # PERF BUG #3b
    partner_id = fields.Many2one("res.partner", string="Customer", index=False)

    state = fields.Selection(
        [
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("waiting", "Waiting"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    priority = fields.Selection(
        [("0", "Low"), ("1", "Normal"), ("2", "High"), ("3", "Urgent")],
        default="1",
    )
    description = fields.Text()
    sla_deadline = fields.Datetime()
    is_late = fields.Boolean()
    sla_note = fields.Char(help="Human-readable SLA status, refreshed by the cron.")
    tag_ids = fields.Many2many("insider.ticket.tag", string="Tags")
    duplicate_of_id = fields.Many2one("insider.ticket", string="Duplicate of")

    # PERF BUG #6
    screenshot = fields.Binary(attachment=False)

    # PERF BUG #7
    partner_ticket_count = fields.Integer(
        compute="_compute_partner_ticket_count",
        store=True,
        help="How many tickets this customer has in total.",
    )

    @api.depends("partner_id.insider_ticket_ids")
    def _compute_partner_ticket_count(self):
        for ticket in self:
            ticket.partner_ticket_count = len(ticket.partner_id.insider_ticket_ids)

    # PERF BUG #8
    @api.depends("reference", "name", "partner_id")
    def _compute_display_name(self):
        for ticket in self:
            open_ct = self.env["insider.ticket"].search_count(
                [
                    ("partner_id", "=", ticket.partner_id.id),
                    ("state", "not in", ("done", "cancelled")),
                ]
            )
            ticket.display_name = (
                f"{ticket.reference or '?'} - {ticket.name} ({open_ct} open)"
            )

    # PERF BUG #1
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("reference"):
                vals["reference"] = (
                    self.env["ir.sequence"].next_by_code("insider.ticket") or "TKT-???"
                )
        tickets = super().create(vals_list)
        # "Auto-escalation": if the customer already has open urgent
        # tickets, bump this one too.
        for ticket in tickets:
            if not ticket.partner_id:
                continue
            urgent = self.search(
                [
                    ("partner_id", "=", ticket.partner_id.id),
                    ("priority", "=", "3"),
                    ("state", "not in", ("done", "cancelled")),
                    ("id", "not in", tickets.ids),
                ],
                limit=1,
            )
            if urgent:
                ticket.write({"priority": "3"})
        return tickets

    # PERF BUG #9
    def write(self, vals):
        res = super().write(vals)
        # "Resolution insights": when tickets get closed, log how the
        # customer's resolved pile is growing.
        if vals.get("state") == "done":
            for ticket in self:
                done_ct = self.env["insider.ticket"].search_count(
                    [
                        ("partner_id", "=", ticket.partner_id.id),
                        ("state", "=", "done"),
                    ]
                )
                _logger.info(
                    "Ticket %s closed; customer now has %s resolved tickets",
                    ticket.reference,
                    done_ct,
                )
        return res

    # PERF BUG #10
    @api.constrains("reference")
    def _check_reference_unique(self):
        for ticket in self:
            if not ticket.reference:
                continue
            duplicates = self.search_count(
                [("reference", "=", ticket.reference), ("id", "!=", ticket.id)]
            )
            if duplicates:
                raise ValidationError(
                    self.env._(
                        "Reference %s is already used by another ticket.",
                        ticket.reference,
                    )
                )

    # PERF BUG #4
    def action_find_similar(self):
        self.ensure_one()
        needle = (self.name or "")[:12]
        similar = self.search([("name", "ilike", needle), ("id", "!=", self.id)])
        return {
            "type": "ir.actions.act_window",
            "name": "Similar tickets",
            "res_model": "insider.ticket",
            "view_mode": "list,form",
            "domain": [("id", "in", similar.ids)],
        }

    # PERF BUG #5
    @api.model
    def _cron_check_sla(self):
        now = fields.Datetime.now()
        all_tickets = self.search([])
        open_tickets = all_tickets.filtered(
            lambda t: t.state in ("new", "in_progress", "waiting")
        )
        for ticket in open_tickets:
            late = bool(ticket.sla_deadline and ticket.sla_deadline < now)
            if ticket.sla_deadline:
                hours = (now - ticket.sla_deadline).total_seconds() / 3600
                status = f"late by {hours:.1f}h" if late else f"due in {-hours:.1f}h"
            else:
                status = "no deadline"
            note = f"{status} (checked {now:%Y-%m-%d %H:%M})"
            ticket.write({"is_late": late, "sla_note": note})
        _logger.info("SLA cron: checked %s tickets one by one", len(open_tickets))

    @api.model
    def generate_demo_data(self, n_of_batches=100, batch_size=500):
        partners = self.env["res.partner"].search([], limit=500)
        if not partners:
            raise ValueError("No partners found, install some demo data first.")
        tags = self.env["insider.ticket.tag"].search([])
        states = ["new", "in_progress", "waiting", "done", "cancelled"]
        subjects = [
            "Cannot login since update",
            "Invoice PDF is empty",
            "Stock levels wrong after inventory",
            "Website checkout error 500",
            "Email templates not rendering",
            "Slow list view in sales",
            "Access rights issue on project",
            "Barcode scanner not recognized",
            "Payroll computation mismatch",
            "Cron job seems stuck",
        ]
        for i in range(n_of_batches):
            self.create(
                [{
                    "name": f"{random.choice(subjects)} [{i}]",
                    "partner_id": random.choice(partners.ids),
                    "state": random.choice(states),
                    "priority": random.choice(["0", "1", "1", "2", "3"]),
                    "sla_deadline": fields.Datetime.add(
                        fields.Datetime.now(), days=random.randint(-10, 10)
                    ),
                    "tag_ids": [(6, 0, random.sample(tags.ids, k=min(2, len(tags))))]
                    if tags
                    else False,
                }
                for x in range(batch_size)
                ]
            )
            _logger.info("Generated %s/%s tickets", i, n_of_batches)
        return True
