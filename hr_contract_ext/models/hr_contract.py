# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from __future__ import division
import datetime
import time

from odoo import SUPERUSER_ID
# from odoo.osv import fields, osv
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import datetime
import calendar
# import workdays
from workdays import workday
from workdays import networkdays
# import NETWORKDAYS
from datetime import datetime
from datetime import timedelta
# from dateutil import relativedelta
from dateutil import relativedelta
# from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import date
import calendar
# import workdays
from workdays import workday
from workdays import networkdays


# class hr_contract(models.Model):
#     _inherit = 'hr.contract'
#
#     grade_step = fields.Many2one('grade.step', 'Grade/Step', domain="[('salary_structure','=',struct_id)]",
#                                  required=False)

class HRContract(models.Model):
    _description = 'Contract'
    _inherit = 'hr.contract'

    # @api.multi  # if these fields are changed, call method
    # @api.depends('interdiction')
    # @api.onchange('actual_pay','pay_month')
    @api.depends('actual_month', 'pay_month')
    def _compute_first(self):
        today = date.today()
        day, num_days = calendar.monthrange(today.year, today.month)
        date_start_obj = date(today.year, today.month, 1)
        # date_end_obj = date(2013, 7, 18)
        date_end_obj = date(today.year, today.month, num_days)

        holidays = []

        net_day = networkdays(date_start_obj, date_end_obj, holidays)
        # work_day = workday(date_start_obj,num_days,[holidays])

        try:
            self.actual_month = net_day
            self.pay_month = net_day
            # self.pay_day = net_day
        except:
            raise UserError("Not Working")
        # day, num_days = calendar.monthrange(today.year, today.month)
        # last_week = num_days % 7
        # last_day = (day + last_week) % 7

        # raise UserError(net_day)
        # return {'value': {self.actual_month: net_day, self.pay_month: net_day}}
        # for obj in self:
        #     obj.actual_month = net_day
        #     obj.pay_month = net_day
        #     obj.actual_day = net_day
        #     obj.pay_day = net_day
        # return {'value': {obj.actual_month: net_day, obj.pay_month: net_day}}

    @api.model
    # @api.onchange('actual_day', 'actual_month')
    def _default_date(self):
        today = date.today()
        day, num_days = calendar.monthrange(today.year, today.month)
        day, num_day = calendar.monthrange(today.year, today.month)
        date_start_obj = date(today.year, today.month, 1)
        # date_end_obj = date(2013, 7, 18)
        date_end_obj = date(today.year, today.month, num_days)

        holidays = []

        net_day = networkdays(date_start_obj, date_end_obj, holidays)
        # for d in self:
        #     d.actual_day = net_day
        # self.actual_month = d.actual_day
        # raise UserError(num_day)

    @api.depends('interdiction')
    def _default_days(self):
        # raise UserError('H')
        today = date.today()
        day, num_days = calendar.monthrange(today.year, today.month)
        day, num_day = calendar.monthrange(today.year, today.month)
        date_start_obj = date(today.year, today.month, 1)
        # date_end_obj = date(2013, 7, 18)
        date_end_obj = date(today.year, today.month, num_days)

        holidays = []

        net_day = networkdays(date_start_obj, date_end_obj, holidays)
        self.actual_day = net_day
        # raise UserError(self.actual_day)

    employee_union = fields.Many2one('emp.union', 'Union')
    staff_class = fields.Many2one('tsa.rate', 'Staff Category')
    employee_number = fields.Char('Employee Number', required=True)
    tsa = fields.Float('TSA', digits_compute=dp.get_precision('Payroll'))
    tsa_rate = fields.Float('TSA Rate')
    ltg = fields.Float('LTG', digits_compute=dp.get_precision('Payroll'))
    ltg_date = fields.Date('Date of LTG')
    ltg_month = fields.Integer('Month of LTG')
    ltg_year = fields.Integer('Year of LTG')
    ltg_date = fields.Date('Date of Employment')
    # 'staff_class =fields.Char('Staff Category')
    job_title = fields.Char('Job Position')
    # 'grade_level =fields.Many2one('grade.step', 'Grade/Step')
    tax = fields.Char('Tax')
    grade = fields.Char('Grade')
    step = fields.Char('step')
    cooperative = fields.Float('Cooperative', digits_compute=dp.get_precision('Payroll'))
    ctss = fields.Float('CTSS', digits_compute=dp.get_precision('Payroll'))
    edpa = fields.Float('EDPA', digits_compute=dp.get_precision('Payroll'))
    salary_advance = fields.Float('Salary Advance', digits_compute=dp.get_precision('Payroll'))
    surcharge = fields.Float('Surcharge', digits_compute=dp.get_precision('Payroll'))
    union_due = fields.Float('Union Due', digits_compute=dp.get_precision('Payroll'))
    union_rate = fields.Integer('Union Rate %')
    teacher_due = fields.Float('Teacher Due', digits_compute=dp.get_precision('Payroll'))
    teacher_due_date = fields.Date('Teacher Due Date')
    teacher_due_month = fields.Integer('Teacher Due Month')
    teacher_due_year = fields.Integer('Teacher Due Year')
    teacher_rate = fields.Integer('Teacher Rate %')
    nlc_due = fields.Float('NLC Due', digits_compute=dp.get_precision('Payroll'))
    nlc_rate = fields.Integer('NLC Rate %')
    welfare = fields.Float('Welfare', digits_compute=dp.get_precision('Payroll'))
    loan = fields.Float('Loan', digits_compute=dp.get_precision('Payroll'))
    meal = fields.Float('Meal', digits_compute=dp.get_precision('Payroll'))
    entertainment = fields.Float('Entertaintment', digits_compute=dp.get_precision('Payroll'))
    domestic = fields.Float('Domestic', digits_compute=dp.get_precision('Payroll'))
    arrears = fields.Float('Arrears', digits_compute=dp.get_precision('Payroll'))
    arrears_date = fields.Date('Arrears Date')
    arrears_month = fields.Integer('Arrears Month')
    arrears_year = fields.Integer('Arrears Year')
    arrears_note = fields.Text('Arrears Note')
    learning = fields.Float('Learning', digits_compute=dp.get_precision('Payroll'))
    exams = fields.Float('Exams', digits_compute=dp.get_precision('Payroll'))
    rent = fields.Float('Rent', digits_compute=dp.get_precision('Payroll'))
    secretariat = fields.Float('Secretariat', digits_compute=dp.get_precision('Payroll'))
    special_edu = fields.Float('Special Edu', digits_compute=dp.get_precision('Payroll'))
    special_allowance = fields.Float('Special Allowance', digits_compute=dp.get_precision('Payroll'))
    overpay = fields.Float('Overpay', digits_compute=dp.get_precision('Payroll'))
    overpay_note = fields.Text('Overpay Note')
    call_duty = fields.Float('Call Duty', digits=(16, 2), required=False)
    posting = fields.Float('Technical/Rural Posting', digits=(16, 2), required=False)
    hazard = fields.Float('Hazard', digits=(16, 2), required=False)
    non_clinical = fields.Float('Non Clinical', digits=(16, 2), required=False)
    shift_duty = fields.Float('Shift Duty', digits=(16, 2), required=False)
    specialist = fields.Float('Specialist', digits=(16, 2), required=False)
    magistrate = fields.Float('Magistrate', digits=(16, 2), required=False)
    robbing = fields.Float('Robbing', digits=(16, 2), required=False)
    thrift = fields.Float('Thrift', digits=(16, 2), required=False)
    pension_deduction = fields.Float('Pension Deduction', digits=(16, 2))
    # 'pension':fields.Float('Pension Ded', digits_compute=dp.get_precision('Payroll'))
    # 'pension_rate':fields.Char('Pension Ded Rate')
    weigh = fields.Float('weigh', digits_compute=dp.get_precision('Payroll'))
    # 'weigh =fields.Float('weigh', digits_compute=dp.get_precision('Payroll'))
    transport = fields.Float('Transport', digits=(16, 2), required=False)
    nhs = fields.Float('NHS', digits=(16, 2), required=False)
    interdiction = fields.Selection([('1', 'False'), ('2', 'True')], 'Interdiction', required=False, default='1')
    # actual_day = fields.Float(string='Days in Month', required=True, compute=_default_days)
    actual_month = fields.Integer('Actual Days', required=True)
    pay_month = fields.Integer('No of Days Worked', required=True)
    contract_pay = fields.Float('Contract Pay', required=False)
    grade_step = fields.Many2one('grade.step', 'Grade/Step')
    proj_month = fields.Integer('Days Worked', required=True)
    month_days = fields.Integer('Days of Month', required=True)
    on_projection = fields.Boolean('On Projection', default=False)
    retire_date_by_proj = fields.Date('Projected Date of Retirement', required=False, default=datetime.today())

    @api.onchange('staff_class', 'tsa', 'tsa_rate')
    def change_staff_class(self):
        if self.staff_class.id or self.tsa or self.tsa_rate:
            tsa_set = self.env['tsa.rate'].search([('id', '=', self.staff_class.id)])
            self.tsa_rate = tsa_set.rate / 100
            # raise UserError(tsa_set.rate / 100)
            self.tsa = (tsa_set.rate / 100) * self.wage

    def write(self, vals):

        if vals.get('arrears'):
            # raise UserError('Yes')
            arrears_now = date.today()
            vals['arrears_date'] = arrears_now
            vals['arrears_month'] = arrears_now.month
            vals['arrears_year'] = arrears_now.year

        if vals.get('teacher_due'):
            # raise UserError('Yes')
            teacher_due_now = date.today()
            vals['teacher_due_date'] = teacher_due_now
            vals['teacher_due_month'] = teacher_due_now.month
            vals['teacher_due_year'] = teacher_due_now.year
            # raise UserError(record.arears)
            # if record.name and self.id:
            #     # raise Warning(record.step)
            # self.env.cr.execute("""UPDATE hr_contract SET interdiction = %s, pay_month = %s, actual_month =%s
            #            WHERE employee_id = %s""", (self.interdiction, self.pay_month, self.actual_month, self.id))
        # else:
        #     raise UserError('No Arrears')
        # self.do_something_writefully_different()
        res = super(HRContract, self).write(vals)
        return res

    @api.onchange('union_due', 'union_rate', 'wage')
    def union_due_rate(self):
        # raise UserError( (self.union_rate / 100))
        self.union_due = (self.union_rate / 100) * self.wage

    @api.onchange('union_due', 'nlc_rate', 'nlc_due')
    def union_due_rate(self):
        if self.union_due:
            self.nlc_due = (self.nlc_rate / 100) * self.union_due

    def compute_ltg(self, cr, uid, ids, context=None):
        for payslip in self.browse(cr, uid, ids, context=context):
            emp_id = payslip.employee_id
            emp_obj = self.pool.get('hr.employee').browse(cr, uid, emp_id.id, context=context)
            for emp_data in emp_obj:
                ltg_pay = emp_obj.pay_value
                # ltg_emp_date = datetime.strptime(emp_obj.date_of_first_appt,DEFAULT_SERVER_DATE_FORMAT)
                ltg_emp_date = datetime.strptime(emp_obj.start_date, DEFAULT_SERVER_DATE_FORMAT)
                this_date = datetime.now()
                # if datetime(ltg_emp_date.month) == this_date.month:
                # datetime.strptime("10/06/2014", "%m/%d/%y")
                # if ltg_emp_date >  this_date.month:
                if ltg_emp_date.month == this_date.month and ltg_emp_date.year < this_date.year:
                    # if ltg_emp_date.month == 01:
                    # ltg_to_pay = float((emp_data.pay_value * 0.939394071264929) * 12 * 0.1)
                    ltg_to_pay = float((emp_data.pay_value) * 12 * 0.1)
                else:
                    ltg_to_pay = 0.00
                    # x = (GRADE_FUNC(pay_proc_period_end_date) * 0.939394071264929) * 12 * 0.1

                    # return True
                    # return {'value ={'ltg =float(payslip.employee_id.pay_value * 0.1)}}
                    # return {'value ={'ltg =100.00}}

                    # return self.write(cr, uid, ids, {'ltg =float(payslip.employee_id.pay_value * 0.1)}, context=context)
                    # return self.write(cr, uid, ids, {'ltg =float(emp_data.pay_value * 0.1)}, context=context)
            self.write(cr, uid, [payslip.id], {'ltg': ltg_to_pay, }, context=context)

    def compute_ltg_sql(self, cr, uid, ids, context=None):
        for payslip in self.browse(cr, uid, ids, context=context):
            emp_id = payslip.employee_id
            emp_obj = self.pool.get('hr.employee').browse(cr, uid, emp_id.id, context=context)
            for emp_data in emp_obj:
                ltg_pay = emp_obj.pay_value
                ltg_emp_date = datetime.strptime(emp_obj.start_date, DEFAULT_SERVER_DATE_FORMAT)
                this_date = datetime.now()
                # if datetime(ltg_emp_date.month) == this_date.month:
                # datetime.strptime("10/06/2014", "%m/%d/%y")
                # if ltg_emp_date >  this_date.month:
                if ltg_emp_date.month == this_date.month and ltg_emp_date.year < this_date.year:
                    # if ltg_emp_date.month == 01:
                    ltg_to_pay = float((emp_data.pay_value * 0.939394071264929) * 12 * 0.1)
                else:
                    ltg_to_pay = 0.00
                    # x = (GRADE_FUNC(pay_proc_period_end_date) * 0.939394071264929) * 12 * 0.1

                    # return True
                    # return {'value ={'ltg =float(payslip.employee_id.pay_value * 0.1)}}
                    # return {'value ={'ltg =100.00}}

                    # return self.write(cr, uid, ids, {'ltg =float(payslip.employee_id.pay_value * 0.1)}, context=context)
                    # return self.write(cr, uid, ids, {'ltg =float(emp_data.pay_value * 0.1)}, context=context)
            self.write(cr, uid, [payslip.id], {'ltg': ltg_to_pay, }, context=context)
