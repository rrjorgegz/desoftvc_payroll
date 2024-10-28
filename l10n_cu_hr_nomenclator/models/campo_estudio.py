# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CampoEstudio(models.Model):
    _name = 'campo.estudio'
    _description = 'Campo de estudio'

    name = fields.Char('Campo de estudio', required=True)
    certificado = fields.Many2one(
        'nivel.certificado', string='Nivel de certificado')
