# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CausaBaja(models.Model):
    _name = 'causa.baja'
    _description = 'Causa de la baja'
    
    name = fields.Char('Causa de la baja', required=True)
