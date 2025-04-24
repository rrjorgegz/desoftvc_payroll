from odoo import fields, models


class PartnerMunicipality(models.Model):
    _inherit = "res.partner"

    municipality = fields.Many2one(
        "res.country.state.municipality",
        "Municipio",
        help="Usted puede asociar el municipio",
    )
    agency_ok = fields.Boolean(string="Agencia")
