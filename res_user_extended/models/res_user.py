# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, SUPERUSER_ID


class User(models.Model):
    _inherit = 'res.users'
    _description = 'User Bank'

    employee_bank_account_id = fields.Many2one(related='employee_id.bank_account_id',
                                               string="Employee's Bank", related_sudo=False,
                                               readonly=False)
