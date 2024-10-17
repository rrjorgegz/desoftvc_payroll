from odoo import fields, models, api

class Licencia (models.Model):
    _name = 'comercializador.licencia'
    #_inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nombre_licencia'

    cliente_id = fields.Many2one(comodel_name="comercializador.cliente", string="Cliente", required = True, tracking=True, ondelete='cascade')
    ultima_venta = fields.Date(string= "Ultima venta", required = True)
    fin_subscripcion = fields.Date(string= "Fin subscripción", required = True)
    producto_id = fields.Many2one(comodel_name='comercializador.producto', string="Producto", required = True, tracking=True, ondelete='cascade')
    importe_venta = fields.Float(string="Importe última venta", required = True)
    division_id = fields.Many2one(comodel_name='comercializador.division', string="Division vendedora", required = True, tracking=True, ondelete='cascade')
    nombre_licencia = fields.Char(compute = "_compute_nombre_licencia", string="Licencia" )
    base_datos_related = fields.Char(string="Base datos", related="cliente_id.base_datos" )
    
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id", string="Currency",
                                  readonly=True, required=True)
    
    def generar_licencia(self):
        generar_licencia_id = self.env['comercializador.generar.licencia.wiz'].create({
                    'fecha_fin_subscripcion': 1,
                    'cliente_id': self.cliente_id.id,
                    'producto_id': self.producto_id.id,
                    'division_id': self.division_id.id,
                }).id
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'comercializador.generar.licencia.wiz',
                'name': 'Generar Licencia',
                'view_mode': 'form',
                'view_type': 'form',
                'views': [[False, 'form']],
                'target': 'new',
                'res_id': generar_licencia_id,
            }
        
    @api.constrains('producto_id','division_vendedora','cliente_id')
    def _compute_nombre_licencia(self):
        for rec in self:
            rec.nombre_licencia = rec.division_id.nombre + ' > ' + rec.producto_id.nombre + ' > ' + rec.cliente_id.nombre
