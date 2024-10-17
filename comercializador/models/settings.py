from odoo import fields, models, api
import pymssql


class ComercializadorSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    jar_path = fields.Boolean('Archivo .jar', required=True,
                             config_parameter='res_config_settings_sample.database_name')