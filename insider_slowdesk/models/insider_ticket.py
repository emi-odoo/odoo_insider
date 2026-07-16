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

    name = fields.Char(required=True, index='trigram')

    reference = fields.Char(index='trigram', readonly=True, copy=False)

    partner_id = fields.Many2one("res.partner", string="Customer", index=True)

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

    screenshot = fields.Binary(attachment=True)
    _unique_reference = models.UniqueIndex("(reference)")

    @api.depends("partner_id.insider_ticket_ids")
    def _compute_partner_ticket_count(self):
        for ticket in self:
            ticket.partner_ticket_count = len(ticket.partner_id.insider_ticket_ids)

    @api.depends("reference", "name", "partner_id")
    def _compute_display_name(self):
        open_ct = self.env["insider.ticket"]._read_group(
            [
                ("partner_id", "in", self.partner_id.ids),
                ("state", "not in", ("done", "cancelled")),
            ],
            ["partner_id"],
            ["__count"]
        )
        n_of_tickets_by_contact = dict(open_ct)
        for ticket in self:
            open_ct = n_of_tickets_by_contact.get(ticket.partner_id, 0)
            ticket.display_name = (
                f"{ticket.reference or '?'} - {ticket.name} ({open_ct} open)"
            )

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env.ref('insider_slowdesk.seq_insider_ticket')
        partner_ids = list(set(vals['partner_id'] for vals in vals_list if vals.get('partner_id')))
        urgent_partners = set(dict(self._read_group(
                [
                    ("partner_id", "in", partner_ids),
                    ("priority", "=", "3"),
                    ("state", "not in", ("done", "cancelled")),
                ],
                ['partner_id'],
                ['__count'],
                having=[('__count', '>', 1)],
        )))
        for vals in vals_list:
            if not vals.get("reference"):
                vals["reference"] = (
                    sequence.next_by_id() or "TKT-???"
                )
            if vals.get('partner_id') and vals.get('partner_id') in urgent_partners:
                vals["priority"] = "3"
        return super().create(vals_list)

    def action_find_similar(self):
        self.ensure_one()
        needle = (self.name or "")[:12]
        return {
            "type": "ir.actions.act_window",
            "name": "Similar tickets",
            "res_model": "insider.ticket",
            "view_mode": "list,form",
            "domain": [("name", "ilike", needle), ("id", "!=", self.id)],
        }

    # PERF BUG #5
    @api.model
    def _cron_check_sla(self):
        now = fields.Datetime.now()
        open_tickets = self.search([('state', 'in', ("new", "in_progress", "waiting"))])
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
