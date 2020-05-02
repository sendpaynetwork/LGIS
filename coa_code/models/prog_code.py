from openerp import models, fields, api



# class SYS(models.Model):
#     _name = 'edsg.sys'
#     _description = 'Systetem Configuration'
#


class ProgrammeSegment(models.Model):
    _name = 'programme.segment'
    _description = 'Chart of Account Programme Segment'
    _rec_name = 'code'

    name = fields.Char('Description')
    code = fields.Char('Code')

    @api.model
    def create(self, vals):
        vals['name'] = vals.get('name').upper()
        res = super(ProgrammeSegment, self).create(vals)
        return res