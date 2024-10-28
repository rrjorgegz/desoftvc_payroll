# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DisciplinaryMeasuredTypes(models.Model):
    _name = 'disciplinary.measured.types'
    _description = "Tipo de medida disciplinaria"

    name = fields.Char('Tipo de medida', required=True,)
    order = fields.Integer(string="Grado de severidad", required=True)
