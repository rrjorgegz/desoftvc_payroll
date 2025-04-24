from odoo import fields, models


class OrgPolitics(models.Model):
    _name = "org.politics"
    _description = "Organizaciones políticas"

    name = fields.Char(string="Organización Política", required=True)
