from odoo import models, fields


class OlympicResult(models.Model):
    _name = "olympics.result"
    _description = "Olympic Result"
    _order = "event_id desc, position asc"

    event_id = fields.Many2one("olympics.event", string="Event", required=True)
    athlete_id = fields.Many2one("res.partner", string="Athlete", required=True)
    position = fields.Integer(string="Position", required=True, default=1)

    _sql_constraints = [
        (
            "olympic_result_unique",
            "unique(event_id, position)",
            "There can be only one athlete in a position for an event.",
        )
    ]
