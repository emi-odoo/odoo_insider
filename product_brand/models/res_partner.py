from odoo import api, models, fields
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    brand_ids = fields.One2many('product.brand', 'owner_id' )
                    
