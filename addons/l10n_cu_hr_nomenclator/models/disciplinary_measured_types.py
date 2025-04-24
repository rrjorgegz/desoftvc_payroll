from odoo import fields, models


class DisciplinaryMeasuredTypes(models.Model):
    _name = "disciplinary.measured.types"
    _description = "Tipo de medida disciplinaria"

    name = fields.Char(
        "Tipo de medida",
        required=True,
    )
    order = fields.Integer(string="Grado de severidad", required=True)
