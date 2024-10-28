# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NivelCertificado(models.Model):
    _name = 'nivel.certificado'
    _description = 'Nivel de certificado'

    name = fields.Char('Nivel de certificado', required=True)
    tarifa = fields.Float('Tarifa', default=0, required=True)

