from odoo import fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    
    def action_confirm(self, *args, **kwargs):
        if self.id > 20:
            raise UserError('cannot be validated')
        return super().action_confirm(*args, **kwargs)