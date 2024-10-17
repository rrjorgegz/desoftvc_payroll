from email.policy import default
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
import xlrd
import tempfile
import binascii
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class ProcesarVentasWiz(models.TransientModel):
    _name = "comercializador.procesar.ventas.wiz"

    #filename = fields.Char("Listado ventas con importes distinto a 370")
    ventas_ids = fields.One2many('comercializador.venta.procesar', 'procesar_venta_wiz_id', string="Venta", required=True)
    division_id = fields.Many2one(comodel_name="comercializador.division", string="Division vendedora", required = True, tracking=True, ondelete='cascade')
    producto_id = fields.Many2one(comodel_name="comercializador.producto", string="Producto", required = True, tracking=True, ondelete='cascade')
    
    def button_process_sales(self):
        for venta in self.ventas_ids:
            if venta.es_valida: # cuando la venta es valida la proceso ...
                if venta.pago_mayor: # cunado el dinero es equivalente a mas tiempo de licencena creo un solo cliente y le pongo la fecha de fin de subscripcion
                    importe = float(venta.importe_venta)
                    if venta.tiene_cliente:
                        id_del_cliente = venta.id_del_cliente
                        licencia = self.env['comercializador.licencia'].sudo().search([('cliente_id', '=', id_del_cliente)])
                        licencia.fin_subscripcion = venta.fecha_pago
                        licencia.ultima_venta = venta.fecha_venta
                        licencia.importe_venta = importe
                    else:
                        id_del_cliente = self.env['comercializador.cliente'].create({
                            'nombre': venta.nombre_cliente,
                            'provincia': 'villa_clara',
                        }).id
                        licencia_id = self.env['comercializador.licencia'].create({
                            'cliente_id': id_del_cliente,
                            'ultima_venta': venta.fecha_venta,
                            'producto_id': self.producto_id.id,
                            'importe_venta': importe,
                            'division_id': self.division_id.id,
                            'fin_subscripcion': venta.fecha_pago,
                        }).id
                        
                    venta_id = self.env['comercializador.venta'].create({
                            'fecha_venta': venta.fecha_venta,
                            'importe_venta': importe,
                            'tipo_venta': 'subscripcion',
                            'cliente_id': id_del_cliente,
                            'factura': venta.numero_factura,
                            'codigo_concepto_facturacion': venta.codigo_concepto_facturacion,
                            'division_id': self.division_id.id,
                            'producto_id': self.producto_id.id,
                        }).id
                elif len(venta.base_datos_ids) > 0: #tiene base de datos para crear
                    importe = float(venta.importe_venta)
                    clientes_ids = []
                    if venta.tiene_cliente:
                        for bd in venta.base_datos_ids:
                            if bd.es_operacion:
                                cliente = self.env['comercializador.cliente'].sudo().search([('nombre', '=', venta.nombre_cliente),('base_datos','=',bd.nombre_base_datos)])
                                licencia = self.env['comercializador.licencia'].sudo().search([('cliente_id', '=', cliente.id)])
                                licencia.ultima_venta = venta.fecha_venta
                                licencia.importe_venta = importe
                                licencia.fin_subscripcion = venta.fecha_pago
                        
                        venta_id = self.env['comercializador.venta'].create({
                                'fecha_venta': venta.fecha_venta,
                                'importe_venta': importe,
                                'tipo_venta': 'subscripcion',
                                'cliente_id': cliente.id,
                                'factura': venta.numero_factura,
                                'codigo_concepto_facturacion': venta.codigo_concepto_facturacion,
                                'division_id': self.division_id.id,
                                'producto_id': self.producto_id.id,
                            }).id
                    else:
                        for bd in venta.base_datos_ids:
                            nuevo_cliente_id = self.env['comercializador.cliente'].create({
                                'nombre': venta.nombre_cliente,
                                'provincia': 'villa_clara',
                                'base_datos': bd.nombre_base_datos,
                            }).id
                            clientes_ids.append(nuevo_cliente_id)
                            licencia_id = self.env['comercializador.licencia'].create({
                                'cliente_id': nuevo_cliente_id,
                                'ultima_venta': venta.fecha_venta,
                                'producto_id': self.producto_id.id,
                                'importe_venta': importe,
                                'division_id': self.division_id.id,
                                'fin_subscripcion': venta.fecha_pago,
                            }).id
                        
                        venta_id = self.env['comercializador.venta'].create({
                                'fecha_venta': venta.fecha_venta,
                                'importe_venta': importe,
                                'tipo_venta': 'subscripcion',
                                'cliente_id': clientes_ids[0],
                                'factura': venta.numero_factura,
                                'codigo_concepto_facturacion': venta.codigo_concepto_facturacion,
                                'division_id': self.division_id.id,
                                'producto_id': self.producto_id.id,
                            }).id
                    
        print('A PROCESARRRRR')
    


class VentaProcesar(models.TransientModel):
    _name = "comercializador.venta.procesar"
    _description = "Venta de importe mayor o menor al equivalente a un mes de suscripción."
    
    fecha_venta = fields.Date(string= "Fecha de la venta", required = True)
    nombre_cliente = fields.Char(string="Nombre cliente")
    numero_factura = fields.Char(string="Número factura")
    importe_venta = fields.Float(string="Importe venta")
    es_valida = fields.Boolean(string="Es válida", default=False,
                               compute="_compute_es_valida")
    pago_mayor = fields.Boolean(string="Pago mayor a un mes")
    codigo_concepto_facturacion = fields.Char(string="Código Concepto Factura")
    fecha_pago = fields.Date(string="Fecha fin de subscripción", required=True, default=lambda self: self.get_fecha_pago())
    base_datos_ids = fields.One2many('comercializador.venta.base.datos', 'venta_procesar_id', string="Base datos")
    procesar_venta_wiz_id = fields.Many2one("comercializador.procesar.ventas.wiz", string="Procesar", ondelete="cascade" , required=True)
    id_del_cliente = fields.Integer(string="ID del cliente", default=0)
    tiene_cliente = fields.Boolean(default="False", compute="_compute_tiene_cliente")
    
    @api.depends('id_del_cliente')
    def _compute_tiene_cliente(self):
        for rec in self:
            if rec.id_del_cliente == 0:
                rec.tiene_cliente = False
            else:
                rec.tiene_cliente = True
    
    def get_fecha_pago(self):
        if self.fecha_venta:
            return self.fecha_venta + relativedelta(months=1)
        else:
            return date.today() + relativedelta(months=1)
    
    @api.model
    def create(self, vals):
        print(vals)
        return super(VentaProcesar, self).create(vals)
    
    @api.depends('pago_mayor', 'base_datos_ids')
    def _compute_es_valida(self):
        for rec in self:
            if rec.pago_mayor == True:
                if rec.fecha_venta < rec.fecha_pago + relativedelta(days=1):
                    rec.es_valida = True
                else:
                    rec.es_valida = False
            else:
                if rec.tiene_cliente: 
                    marcado = False
                    for bd in rec.base_datos_ids:
                        if bd.es_operacion:
                            marcado = True
                            rec.es_valida = True
                            break
                    if not marcado:
                        rec.es_valida = False
                else:
                    if len(rec.base_datos_ids) > 0:
                        rec.es_valida = True
                    else:
                        rec.es_valida = False
                    
    """ def write(self, vals):
        temporal = []
        for db in self.base_datos_ids:
            if db.nombre_base_datos not in temporal:
                temporal.append(db.nombre_base_datos)
            else:
                raise UserError(_("El nombre de la base de datos debe ser único!")) """
    
class BaseDatosVenta(models.TransientModel):
    _name = "comercializador.venta.base.datos"
    _description = "Modelo para la base de datos de una venta cuando el cliente se le factura varias base de datos en una misma factura."
    
    venta_procesar_id = fields.Many2one("comercializador.venta.procesar", string="Venta", ondelete="cascade" , required=True)
    nombre_base_datos = fields.Char(string="Nombre de la Base de Datos", required=True)
    es_operacion = fields.Boolean(string="Base de Datos de la operación", default=False)
    tiene_cliente = fields.Boolean(related="venta_procesar_id.tiene_cliente")
    
    
    """ @api.model
    def create(self, vals):
        others_db = self.env['comercializador.venta.base.datos'].sudo().search([('venta_procesar_id', '=', vals.get('venta_procesar_id'))]) 
        print(" OTRASSS >>>>>>>> ", others_db)
        
        return super(BaseDatosVenta, self).create(vals) """
    
    """ def write(self, vals):
        temporal = []
        for db in self.base_datos_ids:
            if db.nombre_base_datos not in temporal:
                temporal.append(db.nombre_base_datos)
            else:
                raise UserError(_("El nombre de la base de datos debe ser único!")) """
    
    """ @api.constrains('nombre_base_datos')
    def _check_uniq_nombre_base_datos(self):
        if not self:
            return
        
        for rec in self:
            others_db = self.env['comercializador.venta.base.datos'].sudo().search([('venta_procesar_id', '=', rec.venta_procesar_id)]) 
            for db in others_db:
                if db.nombre_base_datos == rec.nombre_base_datos:
                    raise UserError(_("El nombre de la base de datos debe ser único!"))
            
            
            
             """