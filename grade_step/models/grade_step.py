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


from odoo.exceptions import except_orm, Warning as UserError
import logging

_logger = logging.getLogger(__name__)

from odoo import models, fields, api, _


class GradeStep(models.Model):
    _name = "grade.step"

    _description = "Grade and Steps"

    _rec_name = 'name'

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

    @api.model
    def create(self, vals):
        if vals.get('grade', False):
            staff_sgl = str(vals['grade'])
            staff_step = str(vals['step'])
            child = str(staff_sgl) + '/' + str(staff_step)
            vals['name'] = child
            vals['staff_sgl'] = staff_sgl
            vals['staff_step'] = staff_step
            # vals['login']= vals['pid']
            # vals['password']= vals['pid']
        else:
            raise except_orm(_('Error!'), _('Grade not valid, so record will not save.'))
            # raise except_orm(_('Error!'), _('PID not valid, so record will not save.'))
        result = super(GradeStep, self).create(vals)
        return result

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

        return locs.name_get()

    name = fields.Char('SGL/STEP', readonly=True)
    # staff_sgl = fields.Char('Grade')
    grade = fields.Char('Grade')
    step = fields.Char('Step')
    salary = fields.Float('Staff Salary', digits=(16, 2), required=False)
    salary_structure = fields.Many2one('hr.payroll.structure', 'Salary Structure', required=False)
    meal = fields.Float('Meal', digits=(16, 2), required=False)
    entertainment = fields.Float('Entertainment', digits=(16, 2), required=False)
    domestic = fields.Float('Domestic', digits=(16, 2), required=False)
    call_duty = fields.Float('Call Duty', digits=(16, 2), required=False)
    posting = fields.Float('Technical/Rural Posting', digits=(16, 2), required=False)
    hazard = fields.Float('Hazard', digits=(16, 2), required=False)
    non_clinical = fields.Float('Non Clinical', digits=(16, 2), required=False)
    shift_duty = fields.Float('Shift Duty', digits=(16, 2), required=False)
    specialist = fields.Float('Specialist', digits=(16, 2), required=False)
    magistrate = fields.Float('Magistrate', digits=(16, 2), required=False)
    robbing = fields.Float('Robbing', digits=(16, 2), required=False)
    rent_pol = fields.Float('Rent Political', digits=(16, 2), required=False)
    utility_pol = fields.Float('Utility Political', digits=(16, 2), required=False)
    domestic_pol = fields.Float('Domestic Political', digits=(16, 2), required=False)
    entertainment_pol = fields.Float('Entertainment Political', digits=(16, 2), required=False)
    constituency = fields.Float('Constituency', digits=(16, 2), required=False)
    pers_assist = fields.Float('Personal Assistance', digits=(16, 2), required=False)
    transport = fields.Float('Transport', digits=(16, 2), required=False)
    newspaper = fields.Float('News Paper', digits=(16, 2), required=False)
    recess = fields.Float('Recess', digits=(16, 2), required=False)

    _order = 'id'
    _sql_constraints = [
        ('grn_unique', 'unique(name,salary_structure)',
         'SGL/STEP Number must be unique! Please check the level and step selected')]
    name_search = location_name_search

    def write(self, vals):

        res = super(GradeStep, self).write(vals)
        # if self.meal:
        #     self.field3 = True
        # id = self.id
        for record in self:
            self.env.cr.execute('''UPDATE hr_contract SET meal = %s, entertainment = %s,
            domestic = %s, call_duty = %s, posting = %s, hazard =%s, non_clinical = %s,
            shift_duty = %s, specialist = %s, magistrate = %s, robbing = %s
            WHERE grade_step = %s''',
                                (record.meal, record.entertainment, record.domestic, record.call_duty, record.posting,
                                 record.hazard, record.non_clinical, record.shift_duty, record.specialist,
                                 record.magistrate, record.robbing,
                                 self.id))
        # self.do_something_writefully_different()
        return res
