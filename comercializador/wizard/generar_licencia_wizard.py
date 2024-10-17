from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
import os
import subprocess

class GenerarLicenciaWiz(models.TransientModel):
    _name = "comercializador.generar.licencia.wiz"

    semilla = fields.Char("Semilla")
    fecha_fin_subscripcion = fields.Integer(string= "Meses de subscripción", required=True)
    licencia_generada = fields.Char("Licencia", readonly=True)
    cliente_id = fields.Many2one(comodel_name="comercializador.cliente", string="Cliente", ondelete='cascade')
    producto_id = fields.Many2one(comodel_name='comercializador.producto', string="Producto", ondelete='cascade')
    division_id = fields.Many2one(comodel_name='comercializador.division', string="Division vendedora", ondelete='cascade')
    
    def button_generar_licencia(self):
        if self.semilla:
            if not self.licencia_generada:
                path = os.path.join(os.path.dirname(__file__), 'generalic2.jar')
                result = subprocess.run(["java -Xmx512m -jar "+path+' '+self.semilla+' '+str(self.fecha_fin_subscripcion)], capture_output=True, shell=True, text=True)
                #cmd = " java -Xmx2048m -Xms256m -jar %s %s %s"%(path,self.semilla,self.fecha_fin_subscripcion)
                #result = subprocess.run(["./home/odoo/addons/desoftvc_payroll/comercializador/wizard/script.sh"], capture_output=True, shell=True, text=True)
                #cmd = "./script.sh"
                #algo = os.system(result.stdout)
                #raise UserError(result.stdout) 
                if result.returncode == 0: 
                    self.licencia_generada = result.stdout
                    generar_licencia_id = self.env['comercializador.historial.licencia'].create({
                            'cliente_id': self.cliente_id.id,
                            'producto_id': self.producto_id.id,
                            'division_id': self.division_id.id,
                            'generated_date': fields.Datetime.now(),
                            'user_id': self._uid,
                        }).id
                else:
                    raise ValidationError('Ha ocurrido un error generando la licencia >'+result.stderr)
        else:
            raise UserError(_("La semilla es obligatoria!"))
        
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'comercializador.generar.licencia.wiz',
                'name': 'Generar Licencia',
                'view_mode': 'form',
                'view_type': 'form',
                'views': [[False, 'form']],
                'target': 'new',
                'res_id': self.id,
            }
            

            