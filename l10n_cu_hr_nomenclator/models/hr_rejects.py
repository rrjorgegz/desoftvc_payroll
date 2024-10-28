# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrRejects(models.Model):
    _name = 'hr.rejects'
    _description = "Rechazo"
    
    name = fields.Char(string="Causa de rechazo")

