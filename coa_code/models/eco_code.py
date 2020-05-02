from openerp import models, fields, api



# class SYS(models.Model):
#     _name = 'edsg.sys'
#     _description = 'Systetem Configuration'
#


class EconomicSegment(models.Model):
    _name = 'economic.segment'
    _description = 'Chart of Account Economic Segment'
    _rec_name = 'code'

    name = fields.Char('Description')
    code = fields.Char('Code')

    @api.model
    def create(self, vals):
        vals['name'] = vals.get('name').upper()
        res = super(EconomicSegment, self).create(vals)
        return res