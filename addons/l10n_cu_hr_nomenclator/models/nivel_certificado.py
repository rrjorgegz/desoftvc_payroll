from odoo import fields, models


class NivelCertificado(models.Model):
    _name = "nivel.certificado"
    _description = "Nivel de certificado"

    name = fields.Char("Nombre", required=True)
    tarifa = fields.Float("Tarifa.", default=0, required=True)
