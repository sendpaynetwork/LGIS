# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from __future__ import division
import time
import logging

_logger = logging.getLogger(__name__)

# External import
import datetime
import calendar
from workdays import networkdays
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
from odoo import models, fields, api, SUPERUSER_ID
from datetime import date

from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import except_orm, Warning as UserError
import odoo.addons.decimal_precision as dp
import psycopg2

(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)
# Define default weekends, but allow this to be overridden at the function level
# in case someone only, for example, only has a 4-day workweek.
default_weekends = (SAT, SUN)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee Information'

    name = fields.Char(string="Employee Name", related='resource_id.name', store=True, readonly=False, tracking=True)
    category_ids = fields.Many2many(
        'hr.employee.category', 'employee_category_rel',
        'emp_id', 'category_id', groups="hr.group_hr_manager",
        string='Tags')
    form_number = fields.Char('Form Number', required=True)
    employee_union = fields.Many2one('emp.union', 'Employee Union', required=False)
    duration_of_service = fields.Integer('Duration of Service', required=False, default=0)
    employee_age = fields.Integer('Employee Age', required=False, default=0)
    salary_structure = fields.Many2one('hr.payroll.structure', 'Salary Structure', required=False, size=64)
    person_type_id = fields.Char('Person ID', required=False)
    person_type_name = fields.Many2one('edsg.person.type', 'Person Type', required=False)
    tier = fields.Selection([('Federal', 'Federal'), ('State', 'State'), ('Local', 'Local')], 'TIER', required=False)
    incremental_month = fields.Selection([('1', 'January'), ('7', 'July')], 'Incremental Month', required=True)
    incremental_year = fields.Integer('Incremental Year', required=False)
    mda = fields.Many2one('hr.mda', 'MDA', required=True)
    work_id = fields.Many2one('state.lga', 'Work LGA', required=False)
    employment_status = fields.Selection(
        [('In Service', 'In Service'), ('Retired', 'Retired'), ('Transfer', 'Transfer'), ('InActive', 'InActive'),
         ('Resignation', 'Resignation'), ('Withdrawal of Service', 'Withdrawal of Service'),
         ('Abscondment', 'Abscondment'), ('Study Leave Without Pay', 'Study Leave Without Pay'),
         ('Study Leave With Pay', 'Study Leave With Pay'), ('Deceased', 'Deceased'), ('Terminate', 'Terminate'),
         ('Pensioner', 'Pensioner')],
        'Employment Status', default='In Service')
    pension_process = fields.Char('Pension Process')
    termination_date = fields.Date('Date of Termination')
    interdiction = fields.Boolean('Interdiction', required=True, default=False)
    actual_month = fields.Integer('Actual Month', required=True)
    pay_month = fields.Integer('No of Days Worked', required=True)
    employee_action_reason = fields.Text('Status Comment')
    retirement_process = fields.Integer('Retirement Process', default=0)
    employee_cat = fields.Selection([('Political Appointment', 'Political Appointment'), ('Political', 'Political'),
                                     ('Non Political', 'Non Political'), ('Contract Staff', 'Contract Staff'),
                                     ('Permanent Staff', 'Permanent Staff'), ('Intern', 'Intern'),
                                     ('Temporal Staff', 'Temporal Staff'), ('N/A', 'N/A'), ('NA', 'NA')],
                                    'Classification')
    ssid = fields.Char('Structure Name', required=False)
    gl = fields.Many2one('grade.step', 'Grade/Step', domain="[('salary_structure','=',salary_structure)]",
                         required=True)
    grade = fields.Char('Grade')
    on_payroll_emp = fields.Boolean('On Payroll', default=False)
    on_create = fields.Boolean('On Create', default=False)
    step = fields.Char('Step', required=True)
    pay_value = fields.Float('Basic Salary', required=True)
    grade_value = fields.Char('Grade Value')
    # bank_account_id = fields.Char('Employee bank salary account')
    bank_account_id = fields.Many2one(
        'res.bank', 'Bank',
        domain="[('id', '!=', False)]",
        groups="hr.group_hr_user,base.group_system",
        tracking=True,
        help='Employee bank salary account')
    bank_account_number = fields.Char('Bank Account Number', required=False)
    bank = fields.Char('Bank')
    bank_branch = fields.Char('Bank Branch', required=False)
    bank_city = fields.Char('Branch City', required=False)
    sort_code = fields.Char('Bank Code', required=False)
    pay_point = fields.Many2one('hr.pay', 'Pay Point', required=False)
    pension_status = fields.Integer('Pensioner Status', required=False, default=0)
    pension_moved = fields.Integer('Pensioner Board', required=False, default=0)
    employee_school_ids = fields.One2many('hr.employee.sch', 'employee_id', string='Employee School Detail')
    date_of_last_promotion = fields.Date('Date of Last Promotion', required=False,
                                         default=lambda *a: time.strftime('%Y-%m-01'))
    date_of_employment = fields.Date('Date of Employment', required=False, default=lambda *a: time.strftime('%Y-%m-01'))
    last_name = fields.Char('Last Name', required=False)
    employee_number = fields.Char('Employee Number', required=False)
    first_name = fields.Char('First Name', required=False)
    middle_name = fields.Char('Middle Name', required=False)
    title = fields.Char('Title')
    state_of_origin = fields.Many2one('res.country.state', 'State of Origin', domain=[('country_id', '=', 164)],
                                      size=64)
    lga_id = fields.Many2one('state.lga', 'LGA of Origin', required=False)
    district_id = fields.Selection(
        [('EDO NORTH', 'EDO NORTH'), ('EDO CENTRAL', 'EDO CENTRAL'), ('EDO SOUTH', 'EDO SOUTH')], 'Senatorial District',
        required=False, select=1)
    retire_date_by_dob = fields.Date('Retire By DOB', required=False, default=datetime.today())
    due_date = fields.Date('Due Date', required=False)
    bvn = fields.Char('BVN')
    office_address = fields.Text('Office Address', required=False)
    date_posted_to = fields.Date('Date Posted to Office', required=False, default=lambda *a: time.strftime('%Y-%m-01'))
    date_posted_next = fields.Date('Next Posting', required=False)
    staff_class = fields.Selection([('Teaching Staff', 'Teaching Staff'), ('Non Teaching Staff', 'Non Teaching Staff')],
                                   'Staff Category')
    home_address = fields.Text('Home Address')
    employee_posted = fields.Boolean('Employee Posted')
    employee_posted_to = fields.Char('Posted To')
    from_biometric = fields.Boolean('Biometric')
    to_retire = fields.Boolean('Do Not Retire', default=False)
    date_imported = fields.Date('Date From Biometric')
    transferred_from = fields.Char('Transferred From')
    on_projection = fields.Boolean('On Projection', default=False)
    retire_date_by_proj = fields.Date('Projected Date of Retirement', required=False, default=datetime.today())
    proj_month = fields.Integer('Days Worked', required=False)
    month_days = fields.Integer('Days of Month', required=False)

    @api.onchange('first_name', 'middle_name', 'last_name')
    def change_first_middle_last(self):
        if self.first_name and self.last_name:
            self.name = self.first_name + ' ' + ' ' + self.last_name

        if self.first_name and self.last_name and self.middle_name:
            self.name = self.first_name + ' ' + ' ' + self.middle_name + ' ' + ' ' + self.last_name
            
    @api.onchange('job_id')
    def change_job_id(self):
        if self.job_id:
            self.job_title = self.job_id.name

    @api.constrains('form_number')
    def _check_name(self):
        partner_rec = self.env['hr.employee'].search(
            [('form_number', '=', self.form_number), ('id', '!=', self.id)])
        if partner_rec:
            raise UserError('Employee with this form number  ' + str(self.form_number) + ' ' + 'exists')

    @api.onchange('employment_status', 'on_payroll_emp')
    def change_employment_status(self):
        if self.employment_status or self.employment_status:
            if self.employment_status != 'In Service':
                self.on_payroll_emp = False
            else:
                self.on_payroll_emp = True

    @api.onchange('actual_month', 'interdiction')  # if these fields are changed, call method
    def change_actual_month_first(self):
        if self.actual_month:
            today = date.today()
            day, num_days = calendar.monthrange(today.year, today.month)
            date_start_obj = date(today.year, today.month, 1)
            date_end_obj = date(today.year, today.month, num_days)

            holidays = []

            net_day = networkdays(date_start_obj, date_end_obj, holidays)

            self.actual_month = net_day
            if self.pay_month > self.actual_month:
                self.pay_month = self.actual_month

    @api.onchange('pay_month', 'interdiction')
    # if these fields are changed, call method
    def change_pay_month_first(self):
        if self.pay_month:
            today = date.today()
            day, num_days = calendar.monthrange(today.year, today.month)
            date_start_obj = date(today.year, today.month, 1)
            # date_end_obj = date(2013, 7, 18)
            date_end_obj = date(today.year, today.month, num_days)

            holidays = []

            net_day = networkdays(date_start_obj, date_end_obj, holidays)
            self.actual_month = net_day
            if self.pay_month > self.actual_month:
                self.pay_month = self.actual_month

    @api.onchange('interdiction')  # if these fields are changed, call method
    def check_interdiction(self):
        today = date.today()
        day, num_days = calendar.monthrange(today.year, today.month)
        date_start_obj = date(today.year, today.month, 1)
        date_end_obj = date(today.year, today.month, num_days)

        holidays = []

        net_day = networkdays(date_start_obj, date_end_obj, holidays)

        if self.interdiction == 1:
            self.pay_month = net_day
        self.actual_month = net_day
        if self.pay_month > self.actual_month:
            self.pay_month = self.actual_month

    @api.onchange('on_projection', 'retire_date_by_proj')  # if these fields are changed, call method
    def check_projection(self):
        today = date.today()
        day, num_days = calendar.monthrange(today.year, today.month)
        date_start_obj = date(today.year, today.month, 1)
        # date_end_obj = date(2013, 7, 18)
        date_end_obj = date(today.year, today.month, num_days)

        holidays = []

        net_day = networkdays(date_start_obj, date_end_obj, holidays)
        ret_proj = datetime.strptime(str(self.retire_date_by_proj), DEFAULT_SERVER_DATE_FORMAT)
        if self.on_projection:
            # self.proj_month = net_day
            self.proj_month = ret_proj.day
        month_days_val = net_day
        self.month_days = month_days_val

    def on_create_emp(self):
        self.env.cr.execute("UPDATE hr_employee SET on_create = True")

    # @api.onchange('business_group_id', 'company_id')  # if these fields are changed, call method
    # def check_business_group_id(self):
    #     for record in self:
    #         if self.company_id:
    #             record.company_id = record.company_id

    @api.onchange('last_name', 'middle_name', 'first_name', 'name')  # if these fields are changed, call method
    def check_change(self):
        for record in self:
            if self.last_name and self.first_name:
                record.name = str(record.last_name) + ' ' + str(record.first_name)
            if self.last_name and self.middle_name and self.first_name:
                record.name = str(record.last_name) + ' ' + str(record.middle_name) + ' ' + ' ' + str(record.first_name)

    @api.onchange('date_of_employment', 'birthday', 'retire_date_by_dob',
                  'date_posted_to')
    def onchange_next_step(self):

        if self.date_of_employment and self.birthday:
            self.retire_date_by_dob = (
                    datetime.strptime(self.birthday, DEFAULT_SERVER_DATE_FORMAT) + timedelta(days=21900))
            # self.retire_date_by_hiredate = (
            #         datetime.strptime(self.date_of_employment, DEFAULT_SERVER_DATE_FORMAT) + timedelta(
            #     days=10950))

        # if self.date_posted_to:
        #     start = datetime.strftime(self.date_posted_to, DEFAULT_SERVER_DATE_FORMAT)
        #     self.date_posted_next = start + timedelta(days=1825)

    def onchange_state_origin_id(self):
        if self.state_origin:
            department = self.pool.get('res.country.state').browse(self.state_origin)
            state_origin_id = department.id
            return {'domain': {'lga_id': [('state_id', '=', state_origin_id)]}}

    @api.onchange()
    def onchange_person_type(self):
        if self.person_type_name:
            address = self.env['edsg.person.type'].search([('id', '=',)])
            return {'value': {'person_type_id': address.person_code}}
        else:
            return {'value': {'person_type_id': ''}}
        return {'value': {}}

    @api.onchange('to_retire')
    def on_change_retire(self):
        if self.to_retire:
            # if self.employment_status == 'Retire':
            self.employment_status = 'In Service'
            self.c_status = 0
            self.on_payroll_emp = True

    # @api.multi
    def write(self, vals):
        res = super(HrEmployee, self).write(vals)
        # if self.meal:
        #     self.field3 = True
        # id = self.id
        for record in self:
            sal_val = self.env["grade.step"].search([("id", "=", record.gl.id)])
            if sal_val:
                if record.name and self.id:
                    # raise Warning(record.step)
                    self.env.cr.execute(
                        '''UPDATE hr_contract SET wage = %s, struct_id= %s,
                            grade_step= %s, grade= %s, step= %s, meal= %s,
                            entertainment=%s, domestic=%s, call_duty=%s, posting= %s, hazard= %s,
                            non_clinical=%s,shift_duty=%s, specialist=%s, magistrate= %s, robbing = %s, 
                            interdiction = %s,pay_month = %s, actual_month = %s,on_projection =%s, 
                            retire_date_by_proj=%s,proj_month = %s, month_days = %s
                            WHERE employee_id = %s''',
                        (record.pay_value, record.salary_structure.id, record.gl.id,
                         record.grade, record.step, sal_val.meal, sal_val.entertainment, sal_val.domestic,
                         sal_val.call_duty,
                         sal_val.posting, sal_val.hazard, sal_val.non_clinical, sal_val.shift_duty, sal_val.specialist,
                         sal_val.robbing, sal_val.magistrate, self.interdiction, self.pay_month, self.actual_month,
                         self.on_projection,
                         self.retire_date_by_proj, self.proj_month, self.month_days,
                         self.id))
        return res

    @api.model
    def create(self, vals):
        vals['on_create'] = True
        return super(HrEmployee, self).create(vals)

    @api.onchange('gl', 'step', 'grade', 'pay_value', )  # if these fields are changed, call metho
    def check_change_grade(self):
        if self.gl:
            #     self.field3 = True
            for record in self:
                record.grade_value = str(record.gl.name)
                # raise Warning(len(record.grade_value))
                if len(record.grade_value) > 2:
                    # sal_val = self.env
                    sal_val = self.env["grade.step"].search([("id", "=", record.gl.id)])
                    # sal_val = self.env["grade.step"].search([("name", "=", record.grade_value),("salary_structure", "=", record.grade_value)])
                    if sal_val:
                        record.grade = sal_val.grade
                        record.step = sal_val.step
                        record.pay_value = float(sal_val.salary)
                else:
                    title = "Payroll"
                    # message = schl_add.picking_warn_msg
                    message = ("Record Not Found")

                    warning = {
                        'title': title,
                        'message': message,
                    }
                    return {'warning': warning}

    # @api.onchange('salary_structure','gl', 'step', 'grade', 'pay_value', )  # if these fields are changed, call metho
    @api.onchange('salary_structure')  # if these fields are changed, call metho
    def check_change_structure(self):
        if self.salary_structure.id:
            #     self.field3 = True
            # raise Warning(self.salary_structure.id)
            for record in self:

                sal_val = self.env["hr.payroll.structure"].search([("id", "=", record.salary_structure.id)])
                if sal_val:
                    record.gl = False
                    if not record.gl:
                        record.grade = ''
                        record.step = ''
                        record.pay_value = 0.0
                        record.grade_value = ''
                    return {'domain': {'gl': [('salary_structure', '=', record.salary_structure.id)]}}

    @api.onchange('bank_name')  # if these fields are changed, call method
    def check_change_bank_name(self):
        # if self.gl and self.step:
        if self.bank_name:
            #     self.field3 = True
            for record in self:
                record.bank = str(record.bank_name.name)
                record.sort_code = str(record.bank_name.code)

    def in_service(self, cr, uid, ids, context=None):

        emp_obj = self.pool.get('hr.employee').browse(cr, uid, ids, context=context)
        for emp_data in emp_obj:
            self.write(cr, uid, [emp_data.id],
                       {'employment_status': 'In Service', 'c_status': 0, 'retirement_process': 1, }, context=context)

        return True

    def in_retire(self, cr, uid, ids, context=None):

        emp_obj = self.pool.get('hr.employee').browse(cr, uid, ids, context=context)
        for emp_data in emp_obj:
            # to_retired = emp_data.to_retire
            if not emp_data.to_retire:
                self.write(cr, uid, [emp_data.id],
                           {'employment_status': 'Retired', 'c_status': 1, 'retirement_process': 0,
                            'on_payroll_emp': False, }, context=context)

        return True

    # def in_service(self, cr, uid, ids, context=None):
    #
    #     emp_obj = self.pool.get('hr.employee').browse(cr, uid, ids, context=context)
    #     for emp_data in emp_obj:
    #         self.write(cr, uid, [emp_data.id],
    #                    {'employment_status': 'In Service', 'c_status': 0, 'retirement_process': 1,}, context=context)
    #
    #     return True

    # def in_retire(self, cr, uid, ids, context=None):
    #
    #     emp_obj = self.pool.get('hr.employee').browse(cr, uid, ids, context=context)
    #     for emp_data in emp_obj:
    #         self.write(cr, uid, [emp_data.id],
    #                    {'employment_status': 'Retired', 'c_status': 1, 'retirement_process': 0,}, context=context)
    #
    #     return True

    def in_pension(self, cr, uid, ids, context=None):

        emp_obj = self.pool.get('hr.employee').browse(cr, uid, ids, context=context)
        for emp_data in emp_obj:
            pen_due = emp_data.employment_status
            pen_moved = emp_data.pension_moved
            if pen_due == 'Retired' and pen_moved == 0:
                self.write(cr, uid, [emp_data.id], {'pension_status': 1, }, context=context)
            else:
                raise UserError(
                    _("Employment Status for Employee is still active"))

        return True

    # @api.multi
    def move_pension(self):
        # raise Warning(self.id)
        self.env.cr.execute("SELECT id, name FROM res_company")
        res = self.env.cr.fetchall()
        # raise Warning(res[0])
        # for records in res:
        #     com_value = records[1]
        #     com_id = records[0]
        # #    raise Warning(records[1])
        # # raise Warning('YES')
        # # self.env.cr.execute('''SELECT name_related FROM hr_employee WHERE id = 18149''')
        # # conn_pg = pg.DB(host="localhost", user="postgres", passwd="postgres@101", dbname="PENSION")
        # conn = "host='localhost' user='postgres' password='postgres@101' dbname='BEMIS-DEMO'"
        # conn_2 = "host='172.16.0.113' user='postgres' password='postgres@101' dbname='PENSION-TEST'"
        dbvalued = self.env.cr.dbname
        dbvalue = '' + dbvalued + ''
        # raise UserError(dbvalue)
        for records in res:
            com_value = records[1]
            com_id = records[0]
        #    raise Warning(records[1])
        # raise Warning('YES')
        # self.env.cr.execute('''SELECT name_related FROM hr_employee WHERE id = 18149''')
        # conn_pg = pg.DB(host="localhost", user="postgres", passwd="postgres@101", dbname="PENSION")
        conn = "host='localhost' user='postgres' password='postgres@101' dbname=" + dbvalue
        # raise UserError(conn)
        # conn_2 = "host='172.16.0.113' user='postgres' password='postgres@101' dbname='PENSION-TEST'"
        # conn_2 = "host='172.16.0.113' user='postgres' password='postgres@101' dbname='PENSION-TEST'"
        conn_2 = "host='localhost' user='postgres' password='postgres@101' dbname='PENSION-TEST'"

        conn = psycopg2.connect(conn)
        conn_2 = psycopg2.connect(conn_2)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()
        cursor_2 = conn_2.cursor()

        for empids in self:
            self.env.cr.execute("SELECT id, name_related, resource_id, pay_value, bank_name, bank_account_id,"
                                "duration_of_service, gl, first_name, middle_name, last_name, gender, birthday,"
                                "date_of_birth, sort_code,state_of_origin,"
                                "lga_id,bank_city,bank_branch,address_home, "
                                "form_number, employee_number, mda FROM hr_employee WHERE "
                                "pension_status = 1 AND pension_moved = 0 AND id=%s", (empids.id,))

            records = self.env.cr.fetchall()
            for values in records:
                # raise Warning(com_value)
                # raise Warning(str(values[6]))
                # raise UserError(values[22])
                lga_id = self.env['state.lga'].search([('id', '=', values[16])])
                lga_name = lga_id.name
                state_id = self.env['res.country.state'].search([('id', '=', values[15])])
                state_name = state_id.name
                mda_id = self.env['edsg.mda'].search([('id', '=', values[22])])
                mda_name = mda_id.name
                # raise UserError(mda_name)
                pension_banks = self.env['emp.bank'].search([('id', '=', values[4])])
                terminal_pay = self.env['gratuity.pension'].search([('year_of_service', '=', values[6])])
                gratuity_pay = terminal_pay.gratuity
                # raise UserError(values[6])
                pension_pay = terminal_pay.pension
                # raise UserError(pension_pay)
                allowance_pay = self.env['grade.step'].search([('id', '=', values[7])])
                meal_pay = allowance_pay.meal
                domestic_pay = allowance_pay.domestic
                allowance_contract = self.env['hr.contract'].search([('employee_id', '=', values[0])])
                # raise UserError(allowance_contract.id)
                rent_pay = allowance_contract.rent
                transport_pay = allowance_contract.transport
                # utility_pay = allowance_contract.utility
                utility_pay = float(allowance_contract.wage) * 0.15
                salary_pay = values[3]
                # raise UserError(salary_pay)
                terminal_value = salary_pay + rent_pay + transport_pay + meal_pay + utility_pay + domestic_pay
                # raise UserError(terminal_value)
                gratuity = (gratuity_pay * terminal_value) / 100
                pension = (pension_pay * terminal_value) / 100
                # raise UserError(pension)
                pensioner_bank = pension_banks.name
                str_form_number = values[20]
                cursor_2.execute("SELECT form_number FROM hr_pensioner WHERE form_number =%s ", (str_form_number,))
                # records = self.env.cr.fetchall()
                # raise UserError(pension)
                found_form = cursor_2.fetchall()
                if not found_form:
                    cursor_2.execute("INSERT INTO hr_pensioner(pensioner_name,first_name, middle_name, last_name, name,"
                                     "pensioner_lga,pensioner_bank,pensioner_account,bank_account_id,bank,pay_value,"
                                     "gratuity_value,gender,birthday,date_of_birth,sort_code,state_of_origin,"
                                     "bank_city,bank_branch,address_home,form_number,employee_number, on_payroll,active,create_date, write_date) "
                                     "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                     (
                                         values[1], values[8], values[9], values[10], values[1], com_value,
                                         pensioner_bank,
                                         values[5], values[5], pensioner_bank, pension, gratuity, values[11],
                                         values[12], values[13], values[14],
                                         values[15], values[17], values[18], values[19], values[20], values[20], True,
                                         True, datetime.now(), datetime.now()))
                cursor_2.execute("UPDATE hr_pensioner  SET bank_name = emp_bank.id FROM emp_bank "
                                 "WHERE emp_bank.name = hr_pensioner.pensioner_bank OR emp_bank.code = %s AND "
                                 "hr_pensioner.bank_account_id =%s", (values[14], values[5],))
                cursor_2.execute(
                    "UPDATE hr_pensioner  SET state_of_origin = res_country_state.id FROM res_country_state "
                    "WHERE res_country_state.name = %s "
                    "AND hr_pensioner.bank_account_id =%s", (state_name, values[5],))
                cursor_2.execute("UPDATE hr_pensioner  SET lga_id = state_lga.id, "
                                 "work_lga = state_lga.id FROM state_lga "
                                 "WHERE state_lga.name = %s AND hr_pensioner.bank_account_id = %s",
                                 (com_value, values[5],))
                if mda_name:
                    cursor_2.execute("UPDATE hr_pensioner  SET mda = edsg_mda.id "
                                     "FROM edsg_mda "
                                     "WHERE edsg_mda.name = %s AND hr_pensioner.bank_account_id =%s",
                                     (mda_name, values[5],))
                self.env.cr.execute("INSERT INTO hr_employee_pension(name_related,business_group_id,resource_id,"
                                    "pay_value,gratuity_value,form_number) VALUES(%s,%s,%s,%s,%s,%s)",
                                    (values[1], com_id, values[2], pension, gratuity, values[20]))
                conn_2.commit()
                cursor_2.execute("SELECT id, name, pay_value, gratuity_value FROM hr_pensioner WHERE name = %s",
                                 (values[1],))
                record_pen = cursor_2.fetchall()
                for penvalues in record_pen:
                    cursor_2.execute(
                        "INSERT INTO hr_contract_board(name,employee_id,wage,struct_id,type_id, date_start) "
                        "VALUES(%s,%s,%s,%s,%s,%s)",
                        (penvalues[1], penvalues[0], pension, 2, 1, datetime.now()))
                    cursor_2.execute("UPDATE hr_contract_board  SET company_id = (SELECT id FROM res_company)")
                conn_2.commit()
            self.env.cr.execute("UPDATE hr_employee SET pension_moved = 1,on_payroll_emp = False, "
                                "pension_process = 'Moved',"
                                "employment_status ='Pensioner'"
                                " WHERE pension_status = 1 AND pension_moved = 0 AND id=%s", (empids.id,))
        # print "Connected!\n"


class IncrementalStep(models.Model):
    _name = "incremental.step"
    _description = 'Move Employee Step'

    # @api.multi
    def set_incremental_month(self):
        self.env.cr.execute("""UPDATE hr_employee SET incremental_month = 1 WHERE  (EXTRACT (MONTH FROM 
        date_of_employment) > 7 OR EXTRACT (MONTH FROM date_of_employment) = 1)""")
        self.env.cr.execute("""UPDATE hr_employee SET incremental_month = 7 WHERE  (EXTRACT (MONTH FROM 
        date_of_employment) > 1 AND EXTRACT (MONTH FROM date_of_employment) <= 7)""")
        return True

    # @api.multi
    def incremental_step(self):
        month_value = datetime.today()
        # raise UserError(month_value.month)
        # raise UserError(month_value.year)
        if month_value.month == 1 and month_value.day == 25:
            # raise UserError('Yes')
            # else:
            # raise UserError('No')
            # self.env.cr.execute('''SELECT id, name_related, start_date, gl, salary_structure, salary FROM hr_employee WHERE  (EXTRACT (MONTH FROM (now())) = 1) AND date_part('year',age(start_date)) >= 1''')
            # self.env.cr.execute('''SELECT id, name_related, date_of_employment, gl, salary_structure, pay_value FROM hr_employee WHERE  (EXTRACT (MONTH FROM date_of_employment) > 7 OR EXTRACT (MONTH FROM date_of_employment) = 1) AND incremental_month = 1 AND date_part('year',age(date_of_employment)) >= 1
            # self.env.cr.execute('''SELECT id, name_related, date_of_employment, gl, salary_structure, pay_value FROM hr_employee WHERE  (EXTRACT (MONTH FROM date_of_employment) > 7 OR EXTRACT (MONTH FROM date_of_employment) = 1) AND incremental_year != %s AND incremental_month = 1 AND date_part('year',age(date_of_employment)) >= 1
            # self.env.cr.execute('''SELECT id, name_related, date_of_employment, gl, salary_structure, pay_value FROM hr_employee WHERE  (EXTRACT (MONTH FROM date_of_employment) > 7 OR EXTRACT (MONTH FROM date_of_employment) = 1) AND incremental_month = 1 AND date_part('year',age(date_of_employment)) >= 1
            self.env.cr.execute(
                # '''SELECT id, name_related, date_of_employment, gl, salary_structure, pay_value, incremental_month FROM hr_employee WHERE incremental_month = 1 AND date_part('year',age(date_of_employment)) >= 1 ORDER BY id''')
                '''SELECT id, name_related, date_of_employment, gl, salary_structure, pay_value, incremental_month FROM 
                hr_employee WHERE incremental_month = 1 AND date_part('year',age(date_of_employment)) >= 1 AND 
                incremental_year != %s  ORDER BY id''', (month_value.year,))
            res = self.env.cr.fetchall()
            for values in res:
                # raise UserError(values[0])
                self.env.cr.execute(
                    '''SELECT id, name, grade, step, salary_structure FROM grade_step WHERE id = %s AND 
                    salary_structure=%s''', (values[3], values[4],))
                ret = self.env.cr.fetchall()
                for ret_val in ret:
                    in_grade = int(ret_val[2])
                    in_step = int(ret_val[3])
                    up_step = (in_step + 1)
                    grade_step = str(in_grade) + '/' + str(up_step)
                    # raise UserError(in_grade)
                    # raise UserError(ret_val[1])
                    # raise UserError(grade_step)
                    self.env.cr.execute(
                        '''SELECT id, name, grade, step, salary_structure, salary, meal, entertainment, domestic, call_duty, posting, hazard, non_clinical, shift_duty, 
                        specialist, magistrate, robbing FROM grade_step WHERE name = %s AND 
                        salary_structure=%s''', (grade_step, values[4],))
                    out_grade = self.env.cr.fetchall()
                    # if out_grade:
                    for g_val in out_grade:
                        # raise UserError('Yes')
                        self.env.cr.execute(
                            """UPDATE hr_employee SET pay_value = %s, step = %s, gl = %s, incremental_year = %s WHERE id = %s""",
                            (g_val[5], g_val[3], g_val[0], month_value.year, values[0],))
                        # if value[4] == "GENERAL":
                        self.env.cr.execute("""UPDATE hr_contract SET wage = %s, meal = %s, entertainment = %s,
                                domestic = %s, call_duty = %s, posting = %s, hazard =%s, non_clinical = %s,
                                shift_duty = %s, specialist = %s, magistrate = %s, robbing = %s, grade_step = %s WHERE employee_id = %s""",
                                            (g_val[5], g_val[6], g_val[7], g_val[8], g_val[9], g_val[10], g_val[11],
                                             g_val[12], g_val[13], g_val[14], g_val[15], g_val[16], g_val[0],
                                             values[0],))
                        # else:
                        #    self.env.cr.execute("""UPDATE hr_contract SET wage = %s WHERE employee_id = %s""",
                        #                    (g_val[5], values[0],))
                    # else:
                    #     raise UserError('Employee has reached the last step')

        if month_value.month == 7 and month_value.day == 25:
            # raise UserError('Yes')
            # else:
            # raise UserError('No')
            # self.env.cr.execute('''SELECT id, name_related, date_of_employment, gl, salary_structure, pay_value FROM hr_employee WHERE  (EXTRACT (MONTH FROM date_of_employment) > 1 AND EXTRACT (MONTH FROM date_of_employment) <= 7) AND incremental_year != %s AND incremental_month = 7 AND date_part('year',age(date_of_employment)) >= 1
            # self.env.cr.execute('''SELECT id, name_related, date_of_employment, gl, salary_structure, pay_value FROM hr_employee WHERE  (EXTRACT (MONTH FROM date_of_employment) > 1 AND EXTRACT (MONTH FROM date_of_employment) <= 7)  AND incremental_month = 7 AND date_part('year',age(date_of_employment)) >= 1
            # ''',(month_value.year,))
            # self.env.cr.execute(
            #     '''SELECT id, name_related, date_of_employment, gl, salary_structure, pay_value FROM hr_employee WHERE incremental_month = 10 AND date_part('year',age(date_of_employment)) >= 1 AND incremental_year != %s  ORDER BY id''',(month_value.year,))
            self.env.cr.execute(
                '''SELECT id, name_related, date_of_employment, gl, salary_structure, pay_value FROM hr_employee WHERE  incremental_month = 7 AND date_part('year',age(date_of_employment)) >= 1 AND incremental_year != %s  ORDER BY id''',
                (month_value.year,))
            res = self.env.cr.fetchall()
            for values in res:
                # raise UserError(values[0])
                self.env.cr.execute(
                    '''SELECT id, name, grade, step, salary_structure FROM grade_step WHERE id = %s AND 
                    salary_structure = %s''', (values[3], values[4],))
                ret = self.env.cr.fetchall()
                for ret_val in ret:
                    in_grade = int(ret_val[2])
                    in_step = int(ret_val[3])
                    up_step = (in_step + 1)
                    grade_step = str(in_grade) + '/' + str(up_step)
                    # raise UserError(ret_val[1])
                    # raise UserError(grade_step)
                    self.env.cr.execute(
                        '''SELECT id, name, grade, step, salary_structure, salary, meal, entertainment, domestic, call_duty, posting, hazard, non_clinical, shift_duty, 
                        specialist, magistrate, robbing FROM grade_step WHERE name = %s AND 
                        salary_structure=%s''', (grade_step, values[4],))
                    out_grade = self.env.cr.fetchall()
                    # if out_grade:
                    for g_val in out_grade:
                        # raise UserError('Yes')
                        self.env.cr.execute(
                            """UPDATE hr_employee SET pay_value = %s, step = %s, gl = %s, incremental_year = %s WHERE id = %s""",
                            (g_val[5], g_val[3], g_val[0], month_value.year, values[0],))
                        # if value[4] == "GENERAL":
                        self.env.cr.execute("""UPDATE hr_contract SET wage = %s, meal = %s, entertainment = %s,
                                                    domestic = %s, call_duty = %s, posting = %s, hazard =%s, non_clinical = %s,
                                                    shift_duty = %s, specialist = %s, magistrate = %s, robbing = %s, grade_step = %s WHERE employee_id = %s""",
                                            (g_val[5], g_val[6], g_val[7], g_val[8], g_val[9], g_val[10], g_val[11],
                                             g_val[12], g_val[13], g_val[14], g_val[15], g_val[16], g_val[0],
                                             values[0],))
                        # else:
                        #    self.env.cr.execute("""UPDATE hr_contract SET wage = %s WHERE employee_id = %s""",
                        #                    (g_val[5], values[0],))
        else:
            raise UserError('Not In Incremental Month')


class RetirementRun(models.Model):
    _name = 'retirement.run'
    _description = 'Retiremnet Application Run'

    # @api.multi
    def procure_retire_calculation(self):
        # raise UserError('HELLO')
        # self.env.cr.execute(
        #     '''UPDATE hr_employee SET c_status = 1,retirement_process =0, employment_status = 'Retired',
        #      on_payroll_emp = False WHERE
        #     retirement_process < 1 AND (date_part('year',age(birthday)) >= 60 OR date_part('year',age(date_of_employment)) >=
        #     35)''')
        # self.env.cr.execute(
        #     '''UPDATE hr_employee SET duration_of_service = date_part('year',age(date_of_employment)),employee_age =
        #     date_part('year',age(birthday))''')
        # self.env.cr.execute(
        #     '''UPDATE hr_employee SET c_status = 1,retirement_process =0, employment_status = 'Retired',
        #      on_payroll_emp = False WHERE  retirement_process < 1 AND date_part('year',age(date_of_employment)) > 35''')
        self.env.cr.execute(
            '''UPDATE hr_employee SET duration_of_service = date_part('year',age(date_of_employment)),
            employee_age = date_part('year',age(birthday))''')
        self.env.cr.execute(
            '''UPDATE hr_employee SET c_status = 1,retirement_process =0, employment_status = 'Retired' WHERE 
            retirement_process < 1 AND (date_part('year',age(birthday)) >= 60 OR 
            date_part('year',age(date_of_employment)) >= 35)''')


class DurationRun(models.Model):
    _name = 'duration.run'
    _description = 'Duration Run'

    # @api.multi
    def procure_duration_calculation(self):
        # raise UserError('HELLO')
        self.env.cr.execute(
            '''UPDATE hr_employee SET duration_of_service = date_part('year',age(date_of_employment)),employee_age = 
            date_part('year',age(birthday))''')


# class HR_CONTRACT(models.Model):
#     _inherit = 'hr.contract'
#     _description = 'Extend Contract'


# class PAYROLL_SEQUEENCE(models.Model):
#
#     #_name = 'edsg.employee.stage'
#     _inherit = 'ir.sequence'
#     _description = 'Payslip Sequence'

class MovePensioner(models.Model):
    _name = 'move.pensioner'
    _description = 'Move Employee'

    # @api.one
    def move_to_pensioner(self):
        self.env.cr.execute("SELECT id, name FROM res_company")
        res = self.env.cr.fetchall()
        dbvalued = self.env.cr.dbname
        dbvalue = '' + dbvalued + ''
        # raise UserError(dbvalue)
        for records in res:
            com_value = records[1]
            com_id = records[0]
        #    raise Warning(records[1])
        # raise Warning('YES')
        # self.env.cr.execute('''SELECT name_related FROM hr_employee WHERE id = 18149''')
        # conn_pg = pg.DB(host="localhost", user="postgres", passwd="postgres@101", dbname="PENSION")
        conn = "host='localhost' user='postgres' password='postgres@101' dbname=" + dbvalue
        # raise UserError(conn)
        conn_2 = "host='172.16.0.113' user='postgres' password='postgres@101' dbname='PENSION-TEST'"

        conn = psycopg2.connect(conn)
        conn_2 = psycopg2.connect(conn_2)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()
        cursor_2 = conn_2.cursor()

        self.env.cr.execute("SELECT id, name_related, resource_id, pay_value, bank_name, bank_account_id,"
                            "duration_of_service, gl, first_name, middle_name, last_name, gender, birthday,"
                            "date_of_birth, sort_code,state_of_origin,"
                            "lga_id,bank_city,bank_branch,address_home, "
                            "form_number, employee_number, mda FROM hr_employee WHERE "
                            "pension_status = 1 AND pension_moved = 0")

        records = self.env.cr.fetchall()
        for values in records:
            # raise Warning(com_value)
            # raise Warning(str(values[6]))
            # raise UserError(values[22])
            lga_id = self.env['state.lga'].search([('id', '=', values[16])])
            lga_name = lga_id.name
            state_id = self.env['res.country.state'].search([('id', '=', values[15])])
            state_name = state_id.name
            mda_id = self.env['edsg.mda'].search([('id', '=', values[22])])
            mda_name = mda_id.name
            # raise UserError(mda_name)
            pension_banks = self.env['emp.bank'].search([('id', '=', values[4])])
            terminal_pay = self.env['gratuity.pension'].search([('year_of_service', '=', values[6])])
            gratuity_pay = terminal_pay.gratuity
            # raise UserError(values[6])
            pension_pay = terminal_pay.pension
            allowance_pay = self.env['grade.step'].search([('id', '=', values[7])])
            meal_pay = allowance_pay.meal
            domestic_pay = allowance_pay.domestic
            allowance_contract = self.env['hr.contract'].search([('employee_id', '=', values[0])])
            # raise UserError(allowance_contract.id)
            rent_pay = allowance_contract.rent
            transport_pay = allowance_contract.transport
            # utility_pay = allowance_contract.utility
            utility_pay = float(allowance_contract.wage) * 0.15
            salary_pay = values[3]
            terminal_value = salary_pay + rent_pay + transport_pay + meal_pay + utility_pay + domestic_pay
            gratuity = (gratuity_pay * terminal_value) / 100
            pension = (pension_pay * terminal_value) / 100
            pensioner_bank = pension_banks.name
            cursor_2.execute("INSERT INTO hr_pensioner(pensioner_name,first_name, middle_name, last_name, name,"
                             "pensioner_lga,pensioner_bank,pensioner_account,bank_account_id,bank,pay_value,"
                             "gratuity_value,gender,birthday,date_of_birth,sort_code,state_of_origin,"
                             "bank_city,bank_branch,address_home,form_number,employee_number, on_payroll,active) "
                             "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                             (
                                 values[1], values[8], values[9], values[10], values[1], com_value, pensioner_bank,
                                 values[5],
                                 values[5], pensioner_bank,
                                 pension, gratuity, values[11], values[12], values[13], values[14],
                                 values[15], values[17], values[18], values[19], values[20], values[20], True, True,))
            cursor_2.execute("UPDATE hr_pensioner  SET bank_name = emp_bank.id FROM emp_bank "
                             "WHERE emp_bank.name = hr_pensioner.pensioner_bank OR emp_bank.code = %s", (values[14],))
            cursor_2.execute("UPDATE hr_pensioner  SET state_of_origin = res_country_state.id FROM res_country_state "
                             "WHERE res_country_state.name = %s", (state_name,))
            cursor_2.execute("UPDATE hr_pensioner  SET lga_id = state_lga.id, "
                             "work_lga = state_lga.id FROM state_lga "
                             "WHERE state_lga.name = %s", (com_value,))
            if mda_name:
                cursor_2.execute("UPDATE hr_pensioner  SET mda = edsg_mda.id "
                                 "FROM edsg_mda "
                                 "WHERE edsg_mda.name = %s", (mda_name,))
            self.env.cr.execute("INSERT INTO hr_employee_pension(name_related,business_group_id,resource_id,"
                                "pay_value,gratuity_value,form_number) VALUES(%s,%s,%s,%s,%s,%s)",
                                (values[1], com_id, values[2], pension, gratuity, values[20]))
            conn_2.commit()
            cursor_2.execute("SELECT id, name, pay_value, gratuity_value FROM hr_pensioner WHERE name = %s",
                             (values[1],))
            record_pen = cursor_2.fetchall()
            for penvalues in record_pen:
                cursor_2.execute("INSERT INTO hr_contract_board(name,employee_id,wage,struct_id,type_id, date_start) "
                                 "VALUES(%s,%s,%s,%s,%s,%s)",
                                 (penvalues[1], penvalues[0], pension, 2, 1, datetime.now()))
            conn_2.commit()
        self.env.cr.execute("UPDATE hr_employee SET pension_moved = 1,on_payroll_emp = False, "
                            "pension_process = 'Moved',"
                            "employment_status ='Pensioner'"
                            " WHERE pension_status = 1 AND pension_moved = 0")

        print("Connected!\n")

    # @api.one
    def move_to_central(self):
        self.env.cr.execute("SELECT id, name FROM res_company")
        res = self.env.cr.fetchall()
        # raise Warning(res[0])
        for records in res:
            com_value = records[1]
            com_id = records[0]

        conn = "host='localhost' user='postgres' password='postgres@101' dbname='CENTRAL'"

        conn = psycopg2.connect(conn)
        # conn_2 = psycopg2.connect(conn_2)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM res_company")
        record_pen = cursor.fetchall()
        if record_pen:
            for central_val in record_pen:
                raise UserError(central_val[1])
        else:
            raise UserError('No Data')
        # cursor_2 = conn_2.cursor()
