# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

# Get the logger
_logger = logging.getLogger(__name__)

# External import
import datetime
from datetime import datetime

from dateutil import relativedelta
from odoo import models, fields, api, SUPERUSER_ID
import odoo.addons.decimal_precision as dp


class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    name = fields.Char('Loan Description', required=True)
    employee_id = fields.Many2one('hr.employee', 'Employee Name', required=True)
    department_id = fields.Many2one('hr.department', 'Employee Department')
    job_id = fields.Many2one('hr.job', 'Job Title')
    loan_amount = fields.Float('Loan Amount',  required=True)
    deduction_amount = fields.Float('Deduction Amount',  required=True)
    loan_request_date = fields.Date('Loan Request Date', required=True)
    loan_start_date = fields.Date('Deduction Start', required=True)
    loan_duration = fields.Integer('Duration', required=True)
    loan_end_date = fields.Date('Deduction End', required=True)

    # @api.onchange('loan_start_date','loan_end_date','loan_duration','deduction_amount')  # if these fields are changed, call method
    @api.onchange('loan_start_date', 'loan_end_date', 'loan_duration', 'deduction_amount',
                  'loan_amount')  # if these fields are changed, call method
    def check_change_loan_date(self):
        # if self.gl and self.step:
        if self.loan_start_date and self.loan_end_date:
            #     self.field3 = True
            for record in self:
                d1 = datetime.strptime(record.loan_start_date, "%Y-%m-%d")
                # d1 = datetime.strptime(record.loan_start_date, "%m-%d-%Y")
                d2 = datetime.strptime(record.loan_end_date, "%Y-%m-%d")
                # d2 = datetime.strptime(record.loan_end_date, "%m-%d-%Y")
                d3 = relativedelta.relativedelta(d2, d1)
                # d3 = relativedelta(d2, d1)
                # d3 = abs((d2 - d1))
                # return abs((d2 - d1).days)
                # record.loan_duration = d3.months + 1
                record.loan_duration = (d3.years * 12) + (d3.months)
                # record.loan_duration = (d3.years * 12) + (d3.months + 1)
                if record.loan_duration > 0:
                    record.deduction_amount = int(record.loan_amount / record.loan_duration)


    # if these fields are changed, call method
    def process_hr_scheduler_queue(self):
        _logger.debug('Error')
        # self.env.cr.execute('''UPDATE hr_employee SET c_status = 1''')
        # self.env.cr.execute('''UPDATE hr_employee SET c_status = 1, employment_status = %s  WHERE date_part('year',age(birthday)) >= 60 AND employment_status = %s''',('Retired','In Service'))
        # self.env.cr.execute('''UPDATE hr_employee SET c_status = 1, employment_status = 'Retired' WHERE date_part('year',age(birthday)) >= 60''')
        # self.env.cr.execute('''UPDATE hr_employee SET c_status = 1, employment_status = 'Retired' WHERE date_part('year',age(birthday)) >= 60 AND date_part('year',age(date_of_assumption)) >= 35 ''')
        self.env.cr.execute('''update hr_contract set loan = (select deduction_amount from loan_application where hr_contract.employee_id = loan_application.employee_id and (loan_start_date <= now() and loan_end_date >= now()))
                ''')


class LoanRun(models.Model):
    _name = 'loan.run'
    _description = 'Loan Application Run'

    def procure_calculation(self):
        self.env.cr.execute('''update hr_contract set loan = (select deduction_amount from loan_application where hr_contract.employee_id = loan_application.employee_id and (loan_start_date <= now() and loan_end_date >= now()))
                    ''')
