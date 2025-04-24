from odoo import fields, models


class OrgMilitary(models.Model):
    _name = "org.military"
    _description = "Organizaciones militares"

    name = fields.Char(string="Organización Militar", required=True)
