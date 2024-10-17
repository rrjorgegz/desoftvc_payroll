from odoo import fields, models, api

class Producto (models.Model):
    _name = 'comercializador.producto'
    _rec_name = 'nombre'
    #_inherit = ['mail.thread', 'mail.activity.mixin']

    nombre = fields.Char(string= "Nombre del Producto", required = True, tracking=True)
    version = fields.Char(string="Versión")
    descripcion = fields.Char(string="Descripcion")
    precio_total = fields.Float(string="Precio Venta")
    division_id= fields.Many2one(comodel_name='comercializador.division', string="Division propietaria", required=True, tracking=True, ondelete='cascade')

