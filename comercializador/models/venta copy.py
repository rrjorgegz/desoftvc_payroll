from dateutil.relativedelta import relativedelta
from datetime import datetime , date
from odoo import fields, models , api
from odoo.exceptions import ValidationError
import os, subprocess


class Venta (models.Model):
    _name = 'venta'
    _rec_name = 'nombre_venta'
    #_inherit = ['mail.thread','mail.activity.mixin']

    fecha_venta = fields.Date(string= "Fecha de la venta", required = True)
    periodo_suscripcion = fields.Selection([('1 año','1 año'),('2 años','2 años')], string="Período de suscripción", required = True, tracking=True)
    plazos = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('6','6')],string="Plazos", required = True, tracking=True)
    precio_venta = fields.Float(compute= "_compute_precio_venta", string="Precio de Venta", store= True)
    division_vendedora = fields.Many2one(comodel_name='division', string="Division vendedora", required = True, tracking=True, ondelete='cascade')
    cliente_id = fields.Many2one(comodel_name="cliente", string="Cliente", required = True, tracking=True, ondelete='cascade')
    producto_id = fields.Many2one(comodel_name='producto', string="Producto", required = True, tracking=True, ondelete='cascade')
    nombre_venta = fields.Char(compute = "_compute_nombre_venta", string="Venta" )
    licencia = fields.Char(string="Licencia")

    state = fields.Selection([('asignada','Asignada'),('sin asignar','Sin Asignar')], default='sin asignar', string="Licencia")
    proximo_pago = fields.Date(compute = "_compute_proximo_pago", store=True)
    fecha_difer = fields.Integer(compute="_compute_fecha_difer")
    deuda = fields.Float(compute = "_compute_deuda", store=True)
    fecha_final = fields.Date(compute = "_compute_fecha_final", store=True)

    _sql_constraints = [
        ('campos_unicos', 'UNIQUE(cliente_id,producto_id,division_vendedora)',
         'Ya existe una venta con esas características.')
    ]

    @api.constrains('fecha_venta', 'periodo_suscripcion')
    def _compute_fecha_difer(self):
        for rec in self:
            if rec.fecha_venta > fields.Date.today():
                raise ValidationError('La fecha de venta no puede ser después de la fecha actual')
            else:
                if rec.periodo_suscripcion == '1 año':
                    rec.fecha_difer = 12/(int(rec.plazos))
                else:
                    rec.fecha_difer = 24/(int(rec.plazos))


    @api.constrains('fecha_venta')
    def _compute_proximo_pago(self):
            meses = self.fecha_difer
            fecha_pago = self.fecha_venta + relativedelta(months=+ meses)
            self.proximo_pago = fecha_pago
            #self.deuda += self.precio_venta / (int(self.plazos))


    @api.constrains('fecha_venta')
    def _compute_fecha_final(self):
        if self.periodo_suscripcion == '1 año':
            self.fecha_final = self.fecha_venta + relativedelta(months=+ 12)
        else:
            self.fecha_final = self.fecha_venta + relativedelta(months=+ 24)

    @api.constrains('proximo_pago')
    def _compute_deuda(self):
        self.deuda += self.precio_venta/(int(self.plazos))

    @api.constrains('producto_id','division_vendedora','cliente_id')
    def _compute_nombre_venta(self):
        for rec in self:
            rec.nombre_venta = rec.producto_id.nombre + ' | ' + rec.cliente_id.nombre + ' | ' + rec.division_vendedora.nombre

    #Arreglar
    @api.constrains('producto_id','division_vendedora')
    def _compute_precio_venta(self):
            if self.periodo_suscripcion == '1 año':
                self.precio_venta = self.producto_id.precio_suscripcion
            else:
                self.precio_venta = self.producto_id.precio_total

    def send_email(self):
        template = self.env.ref('Modulo_Comercializador.licencia_mail_template')
        mail_id = self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)
        mail = self.env['mail.mail'].browse(mail_id)
        if mail.state == 'exception' :
            return {
                'name': 'Error al enviar el correo',
                'type': 'ir.actions.act_window',
                'res_model': 'error_correo',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
            }
        else:
            return {
                'name': 'Notificación de correo',
                'type': 'ir.actions.act_window',
                'res_model': 'mensaje_correo',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
            }

    def generar_licencia(self):
        if self.deuda > 0 :
            raise ValidationError('No se puede generar la licencia porque el cliente tiene deudas por pagar.')
        else:
             path = "C:\DISCO_D\TRABAJOS_nuevo\ODOO\server\\addons\Modulo_Comercializador\generalic2.jar"
             path_string = "C:\DISCO_D\TRABAJOS_nuevo\ODOO\server\\addons\Modulo_Comercializador\output.txt"
             producto = self.producto_id.nombre+''
             meses = self.fecha_difer
             cmd = "java>>\"%s\" -jar \"%s\" %s %s"%(path_string,path,producto,meses)
             os.system(cmd)
             with open(path_string,"r") as libro:
                self.licencia=libro.readline()
             #with open(path_string, 'w') as file:
             #  pass
             self.state = "asignada"
             return {
                 'name': 'Notificación de licencia',
                 'type': 'ir.actions.act_window',
                 'res_model': 'mensaje_licencia',
                 'view_mode': 'form',
                 'view_type': 'form',
                 'target': 'new',
             }

    def revisar_deuda(self):
        records = self.env['venta'].search([])
        for rec in records:
            anadir_pago = """INSERT INTO public.pago_historico (tipo,monto,fecha_pago,cliente_id,
								  producto_id,division_vendedora)
	        SELECT tipo,monto,fecha_pago,cliente_id,producto_id,division_vendedora
	        from public.pago where pago.cliente_id = %s and pago.division_vendedora = %s
                        and pago.producto_id = %s""" % (rec.cliente_id.id, rec.division_vendedora.id,
                                                     rec.producto_id.id)

            anadir_venta = """insert into public.venta_historico (fecha_venta, 
            periodo_suscripcion, plazos, division_vendedora, cliente_id,producto_id)
	        select fecha_venta, periodo_suscripcion, plazos, division_vendedora, cliente_id, producto_id
	        from public.venta where venta.cliente_id = %s and venta.division_vendedora = %s
                        and venta.producto_id = %s""" % (rec.cliente_id.id, rec.division_vendedora.id,
                                                     rec.producto_id.id)

            eliminar_venta = """delete from venta where venta.cliente_id = %s and venta.division_vendedora = %s
                        and venta.producto_id = %s""" % (rec.cliente_id.id, rec.division_vendedora.id,
                                                     rec.producto_id.id)
            eliminar_pagos = """delete from pago where pago.cliente_id = %s and pago.division_vendedora = %s
                        and pago.producto_id = %s""" % (rec.cliente_id.id, rec.division_vendedora.id,
                                                     rec.producto_id.id)
            if fields.Date.today() >= rec.fecha_final:
                rec._cr.execute(anadir_pago)
                rec._cr.execute(anadir_venta)
                rec._cr.execute(eliminar_pagos)
                rec._cr.execute(eliminar_venta)
            else:
                if fields.Date.today() >= rec.proximo_pago:
                    rec.state = "sin asignar"
                    rec.licencia = ""
                    rec.proximo_pago += relativedelta(months=+ rec.fecha_difer)

    @api.model
    def create(self, vals):
        #producto = self.env['producto'].browse(vals['producto_id'])
        #deuda = producto.precio_total / (int(vals['plazos']))
        #vals['deuda'] = deuda
        #if not(vals['fecha_venta']):
        #   vals['fecha_venta']= fields.Date.today()

        venta = self.env['venta_historico'].search([('cliente_id','in',[vals['cliente_id']]),
                                          ('producto_id','in',[vals['producto_id']]),
                                          ('division_vendedora','in',[vals['division_vendedora']])])
        if len(venta)!=0:
            if vals['periodo_suscripcion'] == '1 año':
                return super(Venta, self).create(vals)
            else:
                raise ValidationError ('El periodo de suscripcion debe ser de 1 año porque ya existe una venta registrada')
        elif vals['periodo_suscripcion'] == '1 año':
            raise ValidationError ('El periodo de suscripcion debe ser de 2 años porque no ha comprado el producto antes')
        return super(Venta, self).create(vals)

class Mensaje_correo(models.TransientModel):
    _name = 'mensaje_correo'

class Mensaje_licencia(models.TransientModel):
    _name = 'mensaje_licencia'

class Error_correo(models.TransientModel):
    _name = 'error_correo'

