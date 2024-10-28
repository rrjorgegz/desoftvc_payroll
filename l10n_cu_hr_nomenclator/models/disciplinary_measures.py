# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DisciplinaryMeasures(models.Model):
    _name = 'disciplinary.measures'
    _description = "Medida disciplinaria"
    
    name = fields.Char(string="Nombre de la Medida disciplinaria",
                       required=True)
    code = fields.Char(string='Referencia')
    impuesto = fields.Integer('Impuesto', default=0)
    tipo_medida = fields.Many2one(
        'disciplinary.measured.types', 'Tipo de medida')
