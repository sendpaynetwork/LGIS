from odoo import models, fields, api


class TSA(models.Model):
    _name = 'tsa.rate'
    _description = 'TSA'

    name = fields.Char('TSA')
    rate = fields.Float('Rate')
