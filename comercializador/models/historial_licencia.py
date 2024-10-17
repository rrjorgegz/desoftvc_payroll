from odoo import fields, models, api

class HistorialLicencia (models.Model):
    _name = 'comercializador.historial.licencia'
    _rec_name = 'producto_id'

    cliente_id = fields.Many2one(comodel_name="comercializador.cliente", string="Cliente", required = True, tracking=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='Usuario', ondelete='cascade', required=True)
    base_datos = fields.Char(related="cliente_id.base_datos")
    generated_date = fields.Date(string="Fecha de Generación", required=True)
    producto_id = fields.Many2one(comodel_name='comercializador.producto', string="Producto", required = True, tracking=True, ondelete='cascade')
    division_id = fields.Many2one(comodel_name='comercializador.division', string="Division vendedora", required = True, tracking=True, ondelete='cascade')
    
    
    