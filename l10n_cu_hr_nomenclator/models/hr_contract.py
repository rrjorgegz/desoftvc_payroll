# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract' 

    scale_group = fields.Many2one('scale.group',string='Grupo Escala', required=True)

    @api.onchange('scale_group')
    def onchange_scale_group(self):
        self.write({'wage': self.scale_group.salary})
    
    @api.onchange('job_id')
    def onchange_job_id(self):
        self.write({'scale_group': self.job_id.scale_group_id.id})
    
