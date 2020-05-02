from openerp import models, fields, api


class GeoSegment(models.Model):
    _name = 'geo.segment'
    _description = "Chart of Account Geo Segment"
    _rec_name = 'code'

    name = fields.Char('Description')
    code = fields.Char('Code')

    @api.model
    def create(self, vals):
        vals['name'] = vals.get('name').upper()
        res = super(GeoSegment, self).create(vals)
        return res