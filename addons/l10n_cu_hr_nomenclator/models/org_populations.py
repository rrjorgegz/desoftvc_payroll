from odoo import fields, models


class OrgPopulations(models.Model):
    _name = "org.populations"
    _description = "Organizaciones masas"

    name = fields.Char(string="Organización de masas", required=True)
