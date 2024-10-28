from odoo import api, fields, models, exceptions, tools, _
from datetime import datetime


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    first_first_name = fields.Char(string='Primer Nombre')
    second_first_name = fields.Char(string='Segundo Nombre')
    first_last_name = fields.Char(string='Primer Apellido')
    second_last_name = fields.Char(string='Segundo Apellido')

    agency_id = fields.Many2one('res.partner', 'Agencia')
    expediente = fields.Integer(string="Número del expediente", default=00000, required=True)
    org_military_ids = fields.Many2many('org.military', string='Militares')
    org_politic_ids = fields.Many2many('org.politics', string='Politicas')
    org_population_ids = fields.Many2many('org.populations', string='Polulares')

    is_retired = fields.Boolean(string='Está retirado?')
    is_reinstated = fields.Boolean(string='Está reincorporado?')
    retired_date = fields.Date(string='Fecha del retiro')
    type_retired_id = fields.Many2one('classification.retired.workers', string='Tipo de retiro')

    register_date = fields.Date('Fecha de alta')
    discharge_date = fields.Date('Fecha de baja')
    discharge_reason = fields.Many2one(comodel_name='causa.baja', string='Causa de la baja')
    working_ok = fields.Boolean('Es baja', default=True)

    #########################################################
    #               COMPOSICIÓN FÍSICA                      #
    #########################################################
    raza = fields.Selection([('Blanca', 'Blanca'),
                             ('Mestiza', 'Mestiza'),
                             ('Negra', 'Negra'),
                             ('Amarilla', 'Amarilla')], string='Raza')
    estatura = fields.Float(string='Estatura(m)')
    peso = fields.Float(string='Peso(kg)')
    tallaCamisa = fields.Char(string='Talla de camisa', size=5)
    tallaPantalon = fields.Char(string='Talla de pantalón')
    tallaZapato = fields.Char(string='Número de zapato')

    #########################################################
    #               COMPOSICIÓN FAMILIAR                    #
    #########################################################
    padre = fields.Char(string='Nombre del padre')
    madre = fields.Char(string='Nombre de la madre')
    familiar_ext = fields.Boolean(string='Familiares en el extranjero')

    #########################################################
    #               NIVEL DE CERTIFICADO                    #
    #########################################################
    certificado = fields.Many2one('nivel.certificado', string='Nivel de certificado')
    campo_estudio = fields.Many2one('campo.estudio', string='Campo de estudio')
    #########################################################
    #               CHEQUEO MEDICO                          #
    #########################################################
    fecha_ini_chequeo = fields.Date('Dia en que entrega')
    fecha_fin_chequeo = fields.Date('Dia en que expira')
    document_require = fields.Many2many('necesary.docs', string='Documentación necesaria')

    def setCertificate(self):
        self.certificate = self.certificado
        self.study_field = self.campo_estudio


    def _concatFullName(self):
        self.ensure_one()
        ffn = fln = sfn = sln = ''
        if (self.first_first_name):
            ffn = self.first_first_name
        if (self.first_last_name):
            sfn = self.first_last_name
        if (self.second_first_name):
            fln = self.second_first_name
        if (self.second_last_name):
            sln = self.second_last_name
        self.name = ffn.strip() + ' ' + fln.strip() + ' ' + sfn.strip() + ' ' + sln.strip()

        return self.name

    @api.onchange('first_first_name')
    def _getFirst_FirstName(self):
        if self.first_first_name:
            self.first_first_name = self.first_first_name
            self._concatFullName()

    @api.onchange('second_first_name')
    def _getSecond_FirstName(self):
        self._concatFullName()

    @api.onchange('first_last_name')
    def _getFirst_LastName(self):
        if self.first_last_name:
            self.first_last_name = self.first_last_name
            self._concatFullName()

    @api.onchange('second_last_name')
    def _getSecond_LastName(self):
        if self.second_last_name:
            self.second_last_name = self.second_last_name
            self._concatFullName()

    def discharge(self):
        self.ensure_one()
        if self.working_ok == True:
            if not self.discharge_reason:
                raise exceptions.ValidationError(_('Debe llenar la causa de la baja antes de dar baja al trabajador'))

            if not self.discharge_date or datetime.strptime(str(self.discharge_date),
                                                            tools.DEFAULT_SERVER_DATE_FORMAT) > datetime.now():
                raise exceptions.ValidationError(_('Fecha de la baja incorrecta'))
            self.write({'active': False, 'working_ok': False})
        else:
            self.write({'active': True, 'working_ok': True, 'discharge_reason': None, 'discharge_date': None})
