from openerp import models, fields, api



# class SYS(models.Model):
#     _name = 'edsg.sys'
#     _description = 'Systetem Configuration'
#


class FundSegment(models.Model):
    _name = 'fund.segment'
    _description = 'Chart of Account Fund Segment'
    _rec_name = 'code'

    name = fields.Char('Description')
    code = fields.Char('Code')

    @api.model
    def create(self, vals):
        vals['name'] = vals.get('name').upper()
        res = super(FundSegment, self).create(vals)
        return res