# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NecesaryDocs(models.Model):
    _name = 'necesary.docs'
    _description = "Documentos a presentar"

    name = fields.Char(string="Documentos", required=True)

