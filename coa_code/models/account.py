# -*- coding: utf-8 -*-

import time
import math

from odoo.osv import expression
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


# ----------------------------------------------------------
# Accounts
# ----------------------------------------------------------


class AccountAccount(models.Model):
    _inherit = "account.account"
    _description = "COA Extension"

    # code = fields.Char(size=64, required=True, index=True)
    admin = fields.Many2one('admin.segment', required=True, index=True)
    admin_code = fields.Char('Description', required=True)
    economic = fields.Many2one('economic.segment', required=True, index=True)
    #economic_code = fields.Char('Description', required=True)
    functional = fields.Many2one('functional.segment', required=True, index=True)
    #functional_code = fields.Char('Description', required=True)
    programme = fields.Many2one('programme.segment', required=True, index=True)
    #programme_code = fields.Char('Description', required=True)
    fund = fields.Many2one('fund.segment', required=True, index=True)
    #fund_code = fields.Char('Description', required=True)
    geocode = fields.Many2one('geo.segment', required=True, index=True)
    #code_description = fields.Char('Description', required=True)

    @api.onchange('admin', 'economic', 'functional', 'programme', 'fund', 'geocode')
    def on_change_code(self):
        # raise UserError(self.admin_code.code)
        if self.admin:
            #raise UserError(self.admin)
            self.code_description = self.admin.name
            self.admin_code = self.admin.name
        if self.economic:
            self.code_description = self.economic.name
        if self.functional:
            self.code_description = self.functional.name
        if self.programme:
            self.code_description = self.programme.name
        if self.fund:
            self.code_description = self.fund.name
        if self.geocode:
            self.code_description = self.geocode.name
        if self.admin and self.economic and self.functional and self.programme and self.fund and self.geocode:
            self.name = self.admin.name + '.' + self.economic.name + '.' + self.functional.name + '.' + self.programme.name + '.' + self.fund.name + '.' + self.geocode.name
            self.code = self.admin.code + '.' + self.economic.code + '.' + self.functional.code + '.' + self.programme.code + '.' + self.fund.code + '.' + self.geocode.code


# class CrossOveredBudget(models.Model):
#     _inherit = "crossovered.budget.lines"
#     _description = "Budget COA Code"
#
#     budget_code = fields.Many2one('account.account', required=True, index=True)
