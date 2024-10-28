# -*- coding: utf-8 -*-
from odoo import models, api, fields
class PartnerMunicipality(models.Model):
    _inherit = 'res.partner'     
       
    municipality = fields.Many2one('res.country.state.municipality', 'Municipality', help='Usted puede asociar el municipio')
    agency_ok = fields.Boolean(string='Agencia')
