from odoo import models, fields, api


class PersonType(models.Model):
    _name = 'edsg.person.type'
    _description = 'Person Type'

    person_type = fields.Char('Person Type')
    person_code = fields.Char('Code')
