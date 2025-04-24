from odoo import fields, models


class DisciplinaryMeasures(models.Model):
    _name = "disciplinary.measures"
    _description = "Medida disciplinaria"

    name = fields.Char(string="Nombre de la Medida disciplinaria", required=True)
    code = fields.Char(string="Referencia")
    tax = fields.Integer(string="Impuesto", default=0)
    tipo_medida = fields.Many2one(
        "disciplinary.measured.types", string="Tipo de medida"
    )
