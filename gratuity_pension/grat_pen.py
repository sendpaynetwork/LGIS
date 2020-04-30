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
from odoo.exceptions import except_orm, Warning as UserError
import logging
# from odoo.osv import fields, osv

from odoo import tools

_logger = logging.getLogger(__name__)
# from odoo.osv import fields, osv
from odoo import models, fields, api, _


class GratuityPension(models.Model):
    _name = "gratuity.pension"

    _description = "Gratuity and Pension"

    #_rec_name = 'name'

    @api.model
    def location_name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args

        locs = self.search(args, limit=limit)
        if len(locs) == 1:
            child_dom = [('parent_left', '>', locs[0].parent_left), ('parent_left', '<', locs[0].parent_right)]
            child_locs = self.search(child_dom)
            locs = locs + child_locs

        return locs.name_get()

    # def _get_sgl(self, cr, uid, context=None):
    def _get_sgl(self):
        res = []
        for r in range(1, 18):
            res.append(([r, r]))  # My assumption
        return res

    def _get_steps(self):
        # def _get_steps(self, cr, uid, context=None):
        res = []
        for r in range(1, 16):
            res.append(([r, r]))  # My assumption
        return res

    year_of_service = fields.Integer('Year of Service')
    gratuity = fields.Integer('Gratuity Percentage')
    pension = fields.Integer('Pension Percentage')

    _order = 'id'
    _sql_constraints = [
        ('grn_unique', 'unique(year_of_service,gratuity,pension)',
         'Record Already Added! Please check the entries')]
    name_search = location_name_search
