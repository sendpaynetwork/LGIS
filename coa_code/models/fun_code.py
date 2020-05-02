from openerp import models, fields, api


# class SYS(models.Model):
#     _name = 'edsg.sys'
#     _description = 'Systetem Configuration'
#


class FunctionalSegement(models.Model):
    _name = 'functional.segment'
    _description = 'Chart of Account Admin Segment'
    _rec_name = 'code'

    name = fields.Char('Description')
    code = fields.Char('Code')

    @api.model
    def create(self, vals):
        vals['name'] = vals.get('name').upper()
        res = super(FunctionalSegement, self).create(vals)
        return res