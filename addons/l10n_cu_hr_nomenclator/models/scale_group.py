from odoo import api, fields, models


class ScaleGroup(models.Model):
    _name = "scale.group"
    _description = "Grupo Escala"
    _rec_name = "name"

    name = fields.Char("Nombre del Grupo Escala", required=True)
    hour = fields.Integer(string="Hora de Empresa", default=44)
    salary = fields.Float(
        string="Salario",
    )
    currency = fields.Many2one(
        "res.currency",
        "Tipo de moneda",
        required=True,
        readonly=False,
        default=70,
    )
    code_scale_group = fields.Char("ID del Grupo Escala", required=True)
    scale_group_line_ids = fields.One2many(
        "scale.group.line", "scale_group_id", string="Evaluation"
    )

    _sql_constraints = [
        (
            "id_scale_group",
            "unique (id_scale_group)",
            "El ID del Grupo Escala  debe ser único!",
        ),
    ]

    @api.onchange("name", "hour")
    def onchange_code_scale_group(self):
        self.ensure_one()
        self.code_scale_group = f"{self.name}{self.hour}"
