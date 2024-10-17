from dateutil.relativedelta import relativedelta
from datetime import datetime , date
from odoo import fields, models , api
from odoo.exceptions import ValidationError
import os, subprocess


class Venta (models.Model):
    _name = 'comercializador.venta'
    _rec_name = 'nombre_venta'

    fecha_venta = fields.Date(string= "Fecha de la venta", required = True)
    importe_venta = fields.Float(string="Importe de venta", required = True)
    division_id = fields.Many2one(comodel_name="comercializador.division", string="Division vendedora", required = True, tracking=True, ondelete='cascade')
    cliente_id = fields.Many2one(comodel_name="comercializador.cliente", string="Cliente", required = True, tracking=True, ondelete='cascade')
    producto_id = fields.Many2one(comodel_name="comercializador.producto", string="Producto", required = True, tracking=True, ondelete='cascade')
    tipo_venta = fields.Selection([('subscripcion', 'Subscripción al energux'),
                                    ('soporte', 'Soporte Energux')], string="Tipo de Venta", required=True)
    nombre_venta = fields.Char(compute = "_compute_nombre_venta", string="Venta")
    base_datos = fields.Char(related="cliente_id.base_datos")
    factura = fields.Char(string="No. Factura")
    codigo_concepto_facturacion = fields.Char(string="Código Concepto Factura")
    
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id", string="Currency",
                                  readonly=True, required=True)


    @api.constrains('producto_id','division_id','cliente_id')
    def _compute_nombre_venta(self):
        for rec in self:
            rec.nombre_venta = rec.division_id.nombre + ' > ' + rec.producto_id.nombre + ' > ' + rec.cliente_id.nombre

    @api.model
    def create(self, vals):
        #producto = self.env['producto'].browse(vals['producto_id'])
        #deuda = producto.precio_total / (int(vals['plazos']))
        #vals['deuda'] = deuda
        #if not(vals['fecha_venta']):
        #   vals['fecha_venta']= fields.Date.today()

        """ venta = self.env['venta_historico'].search([('cliente_id','in',[vals['cliente_id']]),
                                          ('producto_id','in',[vals['producto_id']]),
                                          ('division_vendedora','in',[vals['division_vendedora']])])
        if len(venta)!=0:
            if vals['periodo_suscripcion'] == '1 año':
                return super(Venta, self).create(vals)
            else:
                raise ValidationError ('El periodo de suscripcion debe ser de 1 año porque ya existe una venta registrada')
        elif vals['periodo_suscripcion'] == '1 año':
            raise ValidationError ('El periodo de suscripcion debe ser de 2 años porque no ha comprado el producto antes') """
        
        
        return super(Venta, self).create(vals)