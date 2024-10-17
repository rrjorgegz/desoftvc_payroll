import re
from odoo.exceptions import ValidationError
from odoo import fields, models, api


class Cliente(models.Model):
    _name = 'comercializador.cliente'
    _rec_name = 'nombre'
    #_inherit = ['mail.thread', 'mail.activity.mixin']

    nombre = fields.Char(string="Nombre del Cliente", required=True, tracking=True)
    reeup = fields.Char(string="Código REEUP", tracking=True)
    direccion = fields.Char(string="Dirección")
    base_datos = fields.Char(string="Base de datos")
    es_central = fields.Boolean(string="Es central", default=True)
    telefono = fields.Integer(string="Teléfono")
    provincia = fields.Selection([('pinar', 'Pinar del Rio'), ('artemisa', 'Artemisa'), ('habana', 'La Habana'),
                                  ('mayabeque', 'Mayabeque'), ('matanzas', 'Matanzas'), ('villa_clara', 'Villa Clara'),
                                  ('cienfuegos', 'Cienfuegos'), ('sancti', 'Sancti Spiritus'),
                                  ('ciego', 'Ciego de Ávila'),
                                  ('camaguey', 'Camaguey'), ('holguin', 'Holguín'), ('tunas', 'Las Tunas'),
                                  ('granma', 'Granma'),
                                  ('santiago', 'Santiago de Cuba'), ('guantanamo', 'Guantánamo'),
                                  ('isla', 'Isla de la Juventud')], string="Provincia", required=True)
    # municipio = fields.Selection(selection='_get_municipio', string="Municipio")
    correo = fields.Char(string="Correo", tracking=True)

    _sql_constraints = [
        ('campos_unicos', 'UNIQUE(nombre,reeup,direccion)',
         'Ya existe un cliente con esas características.'),
        ('validar_telefono', 'CHECK(telefono>99999', 'El telefono debe tener un mínimo de 6 dígitos')
    ]

    @api.constrains('provincia')
    def _get_municipio(self):
        if self.provincia == 'villa_clara':
            return [('hola', 'Hola'), ('pepe', 'Pepe')]
        else:
            return [('hola', 'H'), ('pepe', 'P')]
        # municipios={
        #    'pinar': [('hola','Hola'),('pepe','Pepe')],
        #    'villa_clara': [('santa_clara', 'Santa Clara'),('placetas','Placetas')]
        # }
        # return municipios.get(self.provincia,'pinar')


    @api.onchange('correo')
    def validate_mail(self):
        if self.correo:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.correo)
            if match == None:
                raise ValidationError('El correo electrónico no es válido')
