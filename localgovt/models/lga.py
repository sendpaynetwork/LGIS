# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
# from datetime import date, time, datetime
from datetime import date
from datetime import datetime

import logging

from odoo import tools
from odoo import fields, api, models

_logger = logging.getLogger(__name__)


class StateLGA(models.Model):
    # code
    _name = "state.lga"
    _description = "Local Govt"

    @api.model
    def location_name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args

        locs = self.search(args, limit=limit)
        # if len(locs) == 1:
        #     child_dom = [('parent_left', '>', locs[0].parent_left), ('parent_left', '<', locs[0].parent_right)]
        #     child_locs = self.search(child_dom)
        #     locs = locs + child_locs
        #
        return locs.name_get()
        #return locs

    name = fields.Char('LGA Name', size=30, required=False, help='Administrative divisions of a state.')
    code = fields.Char('LGA Code', size=3, required=False,  help='The lga code in max. four chars.')
    state_id = fields.Many2one('res.country.state', 'State ID', required=True, domain=[('country_id', '=', 163)])
    district_id = fields.Selection(
        [('SUBEB HQ', 'SUBEB HQ'), ('EDO NORTH', 'EDO NORTH'), ('EDO CENTRAL', 'EDO CENTRAL'), ('EDO SOUTH', 'EDO SOUTH'),
         ('NOT AVAILABLE', 'NOT AVAILABLE')],
        'Senatorial District', required=False)

    _order = 'code'
    name_search = location_name_search

    def _get_default_category(self):
        res = self.env['res.country.state'].search([('state_id', '=', self.state_id)])
        return res and res[0] or False

    @api.model
    def create(self, vals):
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super(StateLGA, self).create(vals)

    def write(self, vals):
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super(StateLGA, self).write(vals)


class ResUsers(models.Model):
    _inherit = 'res.users'

    lga_id = fields.Many2one('state.lga', 'Local Govt', multi='address', domain="[('district_id','=', district_id)]", required=False)
    district_id = fields.Selection(
        [('SUBEB HQ', 'SUBEB HQ'), ('EDO NORTH', 'EDO NORTH'), ('EDO CENTRAL', 'EDO CENTRAL'),
         ('EDO SOUTH', 'EDO SOUTH')],
        'Senatorial District', required=False)
