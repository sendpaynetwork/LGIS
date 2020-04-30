from odoo import models, fields, api


class MDA(models.Model):
    _name = 'edsg.mda'
    _description = 'Ministry Department Agency'

    name = fields.Char('MDA')
    code = fields.Char('MDA Code')
    lga_id = fields.Many2one('state.lga', 'LGA')
