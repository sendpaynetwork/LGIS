# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

# import pg

# Get the logger

_logger = logging.getLogger(__name__)

from odoo import models, api, fields

from odoo.exceptions import Warning as UserError

(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)
# Define default weekends, but allow this to be overridden at the function level
# in case someone only, for example, only has a 4-day workweek.
default_weekends = (SAT, SUN)


class EmployeeSchool(models.Model):
    _name = 'hr.employee.sch'
    _description = 'Employee School Information'

    employee_id = fields.Many2one('hr.employee', 'Employee Name')
    school_name = fields.Char('School Name')
    course = fields.Char('Course Name')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    qualification = fields.Char('Class of Degree')

