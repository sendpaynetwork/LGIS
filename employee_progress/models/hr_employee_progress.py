import time
from odoo import models, fields, api, SUPERUSER_ID


class HREmployeeProgress(models.Model):
    # _name = 'per.all.people.f'
    _name = 'hr.employee.progress'
    _description = 'Employee Information'

    salary_structure = fields.Char('Salary Structure')
    employee_id = fields.Integer('Employee ID')
    name = fields.Char('Employee Name')
    employee_number = fields.Char('Employee Number')
    step = fields.Integer('Step')
    old_step = fields.Integer('Previous Step')
    grade = fields.Integer('Grade')
    old_grade = fields.Integer('Previous Grade')
    salary = fields.Float('Salary')
    old_salary = fields.Float('Previous Salary')
    grade_value = fields.Char('Grade Level')
    old_grade_value = fields.Char('Previous Grade Level')
    old_salary_structure = fields.Char('Old Salary Structure', required=False, size=64)
    new_salary_structure = fields.Char('New Salary Structure', required=False, size=64)
    date_modified = fields.Datetime('Date Modified', default=lambda *a: time.strftime("%Y-%m-%d %H:%M:%S"))
    modified_by = fields.Char(string='Modified By')
    company_id = fields.Many2one('res.company', 'Company', required=False)

    def get_cur_user(self):
        return self.pool.get('res.users').browse(self.cr, self.uid, self.uid).name


HREmployeeProgress()
