import time
import odoo
import datetime
from datetime import timedelta
from datetime import datetime
from odoo import models, fields, api, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import except_orm, Warning as UserError
from odoo import tools
from odoo.modules.module import get_module_resource


class HREmployeeUpdate(models.Model):
    # _name = 'per.all.people.f'
    _name = 'hr.employee.update'
    _description = 'Employee Information'

    @api.depends('employee_id')
    def _contracts_count(self):
        Contract = self.env['hr.contract']
        # raise UserError(self.employee_id.id)
        employee_id = Contract.search_count([('employee_id', '=', self.employee_id.id)])
        # active_id = Contract.search([('employee_id', '=', self.employee_id.id)])
        # active_id = self.env.context.get('active_ids')
        # raise UserError(active_id.employee_id)
        # self.contracts_count = employee_id
        # self.contract_count = employee_id
        # self.active_id = active_id
        # return employee_id
        # raise UserError(employee_id)
        # return {
        #     #employee_id: Contract.search_count(cr, SUPERUSER_ID, [('employee_id', '=', employee_id)], context=context)
        #     employee_id: Contract.search_count([('employee_id', '=', self.employee_id.id)])
        #     #for employee_id in self.ids
        #     for employee_id in self.employee_id
        # }

    # contracts_count =  fields.Char(compute='_contracts_count', type='integer', string='Contracts')
    # contract_count =  fields.Char(compute='_contracts_count', type='integer', string='Contracts')
    salary_structure = fields.Many2one('hr.payroll.structure', 'Salary Structure', required=False, size=64)
    employee_id = fields.Many2one('hr.employee', 'Employee ID')
    name = fields.Char('Employee Name')
    employee_number = fields.Char('Employee Number')
    grade_level = fields.Many2one('grade.step', 'Grade/Step', domain="[('salary_structure','=',salary_structure)]",
                                  required=True)
    step = fields.Integer('Step')
    old_step = fields.Integer('Previous Step')
    grade = fields.Integer('Grade')
    old_grade = fields.Integer('Previous Grade')
    salary = fields.Float('Salary')
    old_salary = fields.Float('Previous Salary')
    grade_value = fields.Char('Grade Level')
    old_grade_value = fields.Char('Previous Grade Level')
    date_modified = fields.Datetime('Date Modified', default=lambda *a: time.strftime("%Y-%m-%d %H:%M:%S"))
    modified_by = fields.Many2one('res.users', string='Modified By', default=lambda self: self.env.user)
    modified_by_name = fields.Char('Updated By Name', default=lambda self: self.env.user.name)
    old_salary_structure = fields.Char('Old Salary Structure', required=False, size=64)
    new_salary_structure = fields.Char('New Salary Structure', required=False, size=64)
    salary_structure_id = fields.Integer('Structure Id', required=False, size=64)
    contract_id = fields.Many2one('hr.contract', 'Contract', required=False)
    company_id = fields.Many2one('res.company', 'Company', required=False)

    def get_cur_user(self):
        return self.pool.get('res.users').browse(self.cr, self.uid, self.uid).name

    @api.model
    def create(self, vals):
        # raise UserError(vals.get('salary_structure'))
        # raise UserError(vals.get('salary_structure'))
        # self.env.cr.execute("INSERT INTO hr_employee_progress (salary_structure,employee_id,employee_name,employee_number,grade_level,step,old_step,grade,"
        #                     "old_grade,salary,grade_value,old_grade_value,date_modified,modified_by) VALUES (salary_structure)")
        # return super(HREmployeeUpdate, self).create(vals)
        # self.env.cr.execute(
        #     "INSERT INTO hr_employee_progress (salary_structure,grade_level) VALUES (%s,%s)",(vals.get('salary_structure'),vals.get('grade_level'),))
        # self.env.cr.execute(
        #     "INSERT INTO hr_employee_progress (salary_structure,grade_level) VALUES (%s,%s)",
        #     (vals.get('salary_structure'), vals.get('grade_level'),))
        # return super(HREmployeeUpdate, self).create(vals)
        # return super(HREmployeeUpdate, self).create(vals)
        self.env.cr.execute(
            "INSERT INTO hr_employee_progress (old_salary_structure,new_salary_structure,employee_id,name,employee_number,step,old_step,"
            "grade,old_grade,salary,grade_value,old_grade_value,date_modified,modified_by,old_salary,company_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (vals.get('old_salary_structure'), vals.get('new_salary_structure'), vals.get('employee_id'),
             vals.get('name'), vals.get('employee_number'),
             vals.get('step'), vals.get('old_step'), vals.get('grade'), vals.get('old_grade'), vals.get('salary'),
             vals.get('grade_value'), vals.get('old_grade_value'), vals.get('date_modified'),
             vals.get('modified_by_name'), vals.get('old_salary'),vals.get('company_id'),))
        # return super(HREmployeeUpdate, self).create(vals)
        self.env.cr.execute(
            "UPDATE hr_employee SET gl = %s, pay_value =%s, step = %s, grade = %s, grade_value = %s, salary_structure = %s WHERE id = %s",
            (vals.get('grade_level'),
             vals.get('salary'), vals.get('step'), vals.get('grade'), vals.get('grade_value'),
             vals.get('salary_structure'), vals.get('employee_id'),))
        self.env.cr.execute(
            "SELECT id, name, grade, step, salary_structure, salary, meal, entertainment, domestic, call_duty, posting, hazard, non_clinical, shift_duty, "
            "specialist, magistrate, robbing FROM grade_step WHERE id = %s and salary_structure = %s",
            (vals.get('grade_level'), vals.get('salary_structure_id'),))
        res_found = self.env.cr.fetchall()
        for g_val in res_found:
            self.env.cr.execute(
                "UPDATE hr_contract SET grade_step = %s, wage =%s, step = %s, grade = %s, struct_id = %s, meal= %s, entertainment=%s,"
                " domestic=%s, call_duty=%s, posting= %s, hazard= %s,non_clinical=%s,shift_duty=%s, specialist=%s, magistrate= %s, robbing = %s "
                "WHERE employee_id = %s", (
                    vals.get('grade_level'), vals.get('salary'), vals.get('step'), vals.get('grade'),
                    vals.get('salary_structure'), g_val[6], g_val[7], g_val[8], g_val[9], g_val[10], g_val[11],
                    g_val[12], g_val[13], g_val[14], g_val[15], g_val[16], vals.get('employee_id'),))

            self.env.cr.execute("UPDATE hr_contract SET tsa = tsa_rate * wage WHERE employee_id = %s",
                                (vals.get('employee_id'),))

        # self.env.cr.execute("""INSERT INTO hr_employee_progress (old_salary_structure,new_salary_structure,employee_id,employee_name,employee_number,step,old_step,grade,old_grade,salary,grade_value,old_grade_value,date_modified,modified_by)
        # """)
        # self.env.cr.execute("""INSERT INTO hr_employee_progress (old_salary_structure,new_salary_structure,employee_id,employee_name,employee_number,step,old_step,grade,old_grade,salary,grade_value,old_grade_value,date_modified,modified_by)
        # SELECT old_salary_structure,new_salary_structure,employee_id,employee_name,employee_number,step,old_step,grade,old_grade,salary,grade_value,old_grade_value,date_modified,modified_by_name FROM hr_employee_update""")
        return super(HREmployeeUpdate, self).create(vals)

    @api.onchange('employee_id')
    def check_change_employee_id(self):
        # raise UserError(self.employee_id.id)
        # raise UserError(self.contract_id)
        if self.employee_id:
            employee_search = self.env["hr.employee"].search([('id', '=', self.employee_id.id)])
            if employee_search:
                self.employee_number = employee_search.form_number
                self.name = employee_search.name_related
                self.salary_structure = employee_search.salary_structure
                self.grade_level = employee_search.gl.id
                self.old_step = employee_search.step
                self.old_grade = employee_search.grade
                self.old_grade_value = employee_search.grade_value
                self.old_salary_structure = employee_search.salary_structure.name
                self.old_salary = employee_search.pay_value
            contract_search = self.env["hr.contract"].search([('name', '=', self.employee_id.name)])
            if contract_search:
                # raise UserError(self.contract_id)
                self.contract_id = contract_search.id
                # return {'domain': {'contract_id': [('name', '=', contract_search.name)]}}

    @api.onchange('grade_level', 'step', 'grade', 'salary', )  # if these fields are changed, call metho
    def check_change_grade(self):

        # if self.gl and self.step:
        if self.grade_level:
            #     self.field3 = True
            for record in self:
                record.grade_value = str(record.grade_level.name)
                self.salary_structure_id = self.salary_structure.id
                # raise Warning(len(record.grade_value))
                if len(record.grade_value) > 2:
                    # sal_val = self.env
                    sal_val = self.env["grade.step"].search([("id", "=", record.grade_level.id)])
                    # sal_val = self.env["grade.step"].search([("name", "=", record.grade_value),("salary_structure", "=", record.grade_value)])
                    if sal_val:
                        record.grade = sal_val.grade
                        record.step = sal_val.step
                        record.salary = float(sal_val.salary)
                else:
                    title = "Payroll"
                    # message = schl_add.picking_warn_msg
                    message = "Record Not Found"

                    warning = {
                        'title': title,
                        'message': message,
                    }
                    return {'warning': warning}

    @api.onchange('salary_structure')  # if these fields are changed, call metho
    def check_change_structure(self):

        # if self.gl and self.step:
        if self.salary_structure.id:
            self.new_salary_structure = self.salary_structure.name
            self.salary_structure_id = self.salary_structure.id
            #     self.field3 = True
            # raise Warning(self.salary_structure.id)
            for record in self:

                sal_val = self.env["hr.payroll.structure"].search([("id", "=", record.salary_structure.id)])
                # record.grade_value = sal_val.id
                # raise Warning(sal_val)
                if sal_val:
                    record.gl = False
                    if not record.gl:
                        record.grade = ''
                        record.step = ''
                        record.salary = 0.0
                        record.grade_value = ''
                    # raise Warning(sal_val)
                    return {'domain': {'grade_level': [('salary_structure', '=', record.salary_structure.id)]}}


HREmployeeUpdate()
