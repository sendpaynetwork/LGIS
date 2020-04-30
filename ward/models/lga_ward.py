# -*- coding: utf-8 -*-

import re

from openerp import models, fields, api


# ----------------------------------------------------------
# Accounts
# ----------------------------------------------------------


class LGAWard(models.Model):
    _name = "lga.ward"
    _description = "Local Government"

    # code = fields.Char(size=64, required=True, index=True)
    name = fields.Char('Name', required=True, index=True)
    code = fields.Char('Code', required=True, index=True)
    lga_id = fields.Many2one('state.lga', 'LGA', required=True)

    @api.model
    def create(self, vals):
        # re.sub(' +', ' ', self.organisation_id.name)
        vals['name'] = (re.sub(' +', ' ', vals.get('name').upper()))
        vals['code'] = (re.sub(' +', ' ', vals.get('code').upper()))
        res = super(LGAWard, self).create(vals)
        return res
