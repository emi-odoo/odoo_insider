from odoo import models, fields, api


class Olympics(models.Model):
    _name = "olympics.olympics"
    _description = "Olympic"

    name = fields.Char(string="Name", required=True)
    # For each olympics we will have a type, either summer or winter
    # the paralympics are considered as part of the olympics for
    # simplicity sake
    olympics_type = fields.Selection(
        [
            ("summer", "Summer"),
            ("winter", "Winter"),
        ],
        string="Type",
        required=True,
    )
    event_ids = fields.One2many("olympics.event", "olympics_id", string="Events")
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    country_id = fields.Many2one(
        "res.country",
        help="""
        The Olympics might be held in multiple countries, but we will only
        consider the main country here.
        """,
    )
