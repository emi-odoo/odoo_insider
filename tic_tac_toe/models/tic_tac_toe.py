from odoo import fields, models


class TicTacToe(models.Model):
    _name = "tic.tac.toe"
    _description = "Tic Tac Toe"

    player1 = fields.Many2one("res.partner")
    player2 = fields.Many2one("res.partner")
