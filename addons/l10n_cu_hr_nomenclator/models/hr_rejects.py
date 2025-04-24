from odoo import fields, models


class HrRejects(models.Model):
    _name = "hr.rejects"
    _description = "Rechazo"

    name = fields.Char(string="Causa de rechazo")
