from odoo import models, fields, api


class PayPoint(models.Model):
    _name = 'emp.pay'
    _description = 'Pay Point'

    name = fields.Char('Pay POint')
    code = fields.Char('Code')
    mda = fields.Many2one('edsg.mda', 'MDA')
