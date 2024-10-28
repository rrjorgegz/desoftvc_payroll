# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrCategory(models.Model):
    _name = 'hr.category'
    _description = 'Categoría del cargo'

    order = fields.Integer(string='Orden')
    code = fields.Char('Código de la categoría', required=True)
    name = fields.Char('Nombre de la categoría', required=True)
    _sql_constraints = [
        ('code', 'unique (code)', 'El código debe ser único!')
    ]
