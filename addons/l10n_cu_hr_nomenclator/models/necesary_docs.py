from odoo import fields, models


class NecesaryDocs(models.Model):
    _name = "necesary.docs"
    _description = "Documentos a presentar"

    name = fields.Char(string="Documentos", required=True)
