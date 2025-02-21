from odoo import models, fields, api


class TrackOperation(models.Model):
    _name = "track.operation"
    _description = "Track Operation"

    user_id = fields.Many2one("res.users", string="User")
    operation = fields.Char()

    @api.model
    def create_operation(self, operation):
        return self.sudo().create({"user_id": self.env.uid, "operation": operation})
