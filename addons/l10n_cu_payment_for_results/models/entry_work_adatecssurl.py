from datetime import datetime

from odoo import _, api, fields, models


class EntryWorkADATECSsurl(models.Model):
    _name = "entry.work.adatecssurl"
    _description = "Entradas de Trabajo ADATECSsurl"

    name = fields.Char(string="Nombre", default=lambda self: _("New"), required=True)
    date = fields.Date(string="Fecha", required=True, default=datetime.today())
    evaluation_line_ids = fields.One2many(
        "evaluation.employee.adatecssurl", "entry_work_id", string="Evaluaciones"
    )

    @api.model
    def create(self, vals_list):
        if vals_list.get("name", False) in [False, _("New")]:
            vals_list["name"] = self.env["ir.sequence"].next_by_code(
                "entry.work.adatecssurl"
            )
        request = super().create(vals_list)
        return request
