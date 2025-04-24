from odoo import fields, models


class CampoEstudio(models.Model):
    _name = "campo.estudio"
    _description = "Campo de estudio"

    name = fields.Char("Campo de estudio", required=True)
    certificado = fields.Many2one("nivel.certificado", string="Nivel de certificado")
