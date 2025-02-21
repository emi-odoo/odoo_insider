from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    olympic_result_ids = fields.One2many("olympics.result", "athlete_id")
    olympic_event_ids = fields.Many2many(
        "olympics.event", relation="olympics_event_athlete_rel", column1="athlete_id", column2="event_id"
    )
