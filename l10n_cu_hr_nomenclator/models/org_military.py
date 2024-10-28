# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrgMilitary(models.Model):
    _name = 'org.military'
    _description = "Organizaciones militares"

    name = fields.Char(string="Organización Militar",
                       required=True)

