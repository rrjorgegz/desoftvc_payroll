from odoo import fields, models


class HrJob(models.Model):
    _inherit = "hr.job"

    category_id = fields.Many2one(
        "hr.category",
        string="Categoría",
        required=True,
    )
    scale_group_id = fields.Many2one(
        "scale.group",
        string="Grupo escala",
        required=True,
    )
    leader_ok = fields.Boolean("Dirigente", default=False)
