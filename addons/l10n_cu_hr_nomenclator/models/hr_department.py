from odoo import fields, models


class HrDepartment(models.Model):
    _inherit = "hr.department"

    code = fields.Char(string="Código")

    _sql_constraints = [
        ("code_dep_uniq", "unique(code)", "El Código ya de encuentra."),
    ]
