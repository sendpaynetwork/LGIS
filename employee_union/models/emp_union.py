# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import psycopg2

import logging

# Get the logger
_logger = logging.getLogger(__name__)

# External import
from odoo import models, fields, api


class LabourUnion(models.Model):
    _name = 'emp.union'
    _description = 'Labour Union'

    name = fields.Char('Labour Union')
    deduction = fields.Float('Rate %')
    code = fields.Char('Code')
    description = fields.Text('Description')
