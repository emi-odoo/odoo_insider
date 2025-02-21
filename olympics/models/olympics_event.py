from odoo import api, models, fields


class OlympicsEvent(models.Model):
    # for simplicity sake we represent the final event of an olympics
    # discipline as an event
    _name = "olympics.event"
    _description = "Olympic Event"

    name = fields.Char(string="Name", required=True)
    olympics_id = fields.Many2one("olympics.olympics", string="Olympics", required=True)
    datetime_start = fields.Datetime(string="Start Time")
    athlete_ids = fields.Many2many("res.partner", relation="olympics_event_athlete_rel", column1="event_id", column2="athlete_id")
    result_ids = fields.One2many("olympics.result", "event_id", string="Results")

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        string="State",
        required=True,
        default="draft",
    )

    @api.depends("name", "olympics_id")
    def _compute_display_name(self):
        for account in self:
            account.display_name = f"{account.olympics_id.name} - {account.name}"

    @api.model_create_multi
    def create(self, vals_list):
        events = super().create(vals_list)
        for event in events:
            if event.state == "done":
                self.env["bus.bus"]._sendone("olympic_channel", "olympics.event/finished", {"event_id": event.id})
        self.env["bus.bus"]._sendone("olympic_channel", "olympics.event/state_changed", {"event_ids": event.ids})
        return events

    def write(self, vals):
        result = super().write(vals)
        if vals.get("state") == "done":
            for event in self:
                self.env["bus.bus"]._sendone("olympic_channel", "olympics.event/finished", {"event_id": event.id})
        self.env["bus.bus"]._sendone("olympic_channel", "olympics.event/state_changed", {"event_ids": self.ids})
        return result

    def open_result(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "olympics.result",
            "view_mode": "tree",
            "target": "new",
            "domain": [("event_id", "=", self.id)],
            "context": {"default_event_id": self.id},
        }
