# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ClassificationRetiredWorkers(models.Model):
    _name = 'classification.retired.workers'
    _description = 'Clasificacion de las jubilaciones'

    name = fields.Char(string='Jubilación', required=True)

