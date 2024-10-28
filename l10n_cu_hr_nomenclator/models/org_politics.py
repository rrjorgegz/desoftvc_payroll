# -*- coding: utf-8 -*-

from odoo import models, fields, api

 
class OrgPolitics(models.Model):
    _name = 'org.politics'
    _description = "Organizaciones políticas"

    name = fields.Char(string="Organización Política",
                       required=True)
