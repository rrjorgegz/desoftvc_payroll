# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrgPopulations(models.Model):
    _name = 'org.populations'
    _description = "Organizaciones masas"
    
    name = fields.Char(string="Organización de masas",
                       required=True)
