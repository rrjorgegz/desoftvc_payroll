from odoo import fields, models


class ClassificationRetiredWorkers(models.Model):
    _name = "classification.retired.workers"
    _description = "Clasificacion de las jubilaciones"

    name = fields.Char(string="Jubilación", required=True)
