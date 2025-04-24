from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ScaleGroupLine(models.Model):
    _name = "scale.group.line"
    _description = "Grupo Escala Line"

    hour = fields.Integer(string="Hora de Empresa", default=44)
    salary = fields.Float(
        string="Salario",
    )
    currency = fields.Many2one(
        "res.currency", "Tipo de moneda", required=True, readonly=False, default=70
    )
    eval_start = fields.Float(string="Evaluation Start", default=0)
    eval_end = fields.Float(string="Evaluation End", default=0)
    scale_group_id = fields.Many2one("scale.group", string="Grupo Escala")

    @api.constrains("eval_start", "eval_end")
    def validate_evaluation(self):
        line = self.scale_group_id.scale_group_line_ids - self
        line_start = line.filtered(
            lambda li: (self.eval_start >= li.eval_start)
            and (self.eval_start <= li.eval_end)
        )
        line_end = line.filtered(
            lambda li: (self.eval_end >= li.eval_start)
            and (self.eval_end <= li.eval_end)
        )
        if len(line_start) > 0:
            raise ValidationError(
                _(
                    """El rango de evaluaición inicial
no puede estar dentro de otra evaluaición."""
                )
            )
        if len(line_end) > 0:
            raise ValidationError(
                _(
                    """El rango de evaluaición final
no puede estar dentro de otra evaluaición."""
                )
            )
