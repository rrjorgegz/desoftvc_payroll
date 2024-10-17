import re
from odoo.exceptions import ValidationError
from odoo import fields, models, api


class Division (models.Model):
    _name = 'comercializador.division'
    _rec_name = 'nombre'
    #_inherit = ['mail.thread', 'mail.activity.mixin']

    nombre = fields.Char(string="Nombre de la Division", required = True, tracking=True)
    comercial_nombre = fields.Char(string="Nombre del Comercial", tracking=True)
    comercial_correo = fields.Char(string="Correo del Comercial", required=True, tracking=True)
    provincia = fields.Selection([('pinar', 'Pinar del Rio'), ('artemisa', 'Artemisa'), ('habana', 'La Habana'),
                                  ('mayabeque', 'Mayabeque'), ('matanzas', 'Matanzas'), ('villa_clara', 'Villa Clara'),
                                  ('cienfuegos', 'Cienfuegos'), ('sancti', 'Sancti Spiritus'),
                                  ('ciego', 'Ciego de Ávila'),
                                  ('camaguey', 'Camaguey'), ('holguin', 'Holguín'), ('tunas', 'Las Tunas'),
                                  ('granma', 'Granma'),
                                  ('santiago', 'Santiago de Cuba'), ('guantanamo', 'Guantánamo'),
                                  ('isla', 'Isla de la Juventud')], string="Provincia", tracking=True, required=True)

    _sql_constraints = [
        ('campos_unicos', 'UNIQUE(nombre,comercial_nombre,comercial_correo, provincia)',
         'Ya existe una division con esas características.')
    ]

    @api.onchange('comercial_correo')
    def validate_mail(self):
        if self.comercial_correo:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.comercial_correo)
            if match == None:
                raise ValidationError('El correo electrónico no es válido')