# -*- coding: utf-8 -*-


from odoo import models, fields, api


class EvaluationEmployeeADATECSsurl(models.Model):
    _name = 'evaluation.employee.adatecssurl'
    _description = 'Evaluación de Empleado ADATECSsurl'

    name = fields.Char('Name',default="New")
    evaluation = fields.Float(string="Evaluación", default=85)
    entry_work_id = fields.Many2one('entry.work.adatecssurl',string='Entradas de Trabajo ADATECSsurl')
    not_employees_ids = fields.Many2many('hr.employee', compute='_compute_not_employees_ids')
    employee_id = fields.Many2one('hr.employee', string='Empleado', domain="[('id','not in',not_employees_ids)]")
    contract_id = fields.Many2one('hr.contract', string='Contrato',domain="[('state','=','open')]",index=True)
    scale_group_id = fields.Many2one('scale.group', string='Grupo Escala')
    wage = fields.Float('Salario',default=0)
    currency_id = fields.Many2one( 'res.currency', string='Moneda',default=70)
    
    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].next_by_code('evaluation.employee.adatecssurl')
        request = super(EvaluationEmployeeADATECSsurl, self).create(vals_list)
        return request

    @api.depends('entry_work_id','employee_id')
    def _compute_not_employees_ids(self):
        for record in self:
            record.not_employees_ids = record.entry_work_id.evaluation_line_ids.mapped(
                lambda c: c.employee_id) 

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.ensure_one()
        result = False
        data = self.env['hr.contract'].search(
            [('employee_id', '=', self.employee_id.id), ('active', '=', True)], limit=1)
        if len(data)>0:
            result= data[0].id
        self.write({'contract_id': result})

    @api.onchange('contract_id')
    def onchange_contract_id(self):
        self.ensure_one()
        self.write({'scale_group_id': self.contract_id.scale_group.id}) 
    
    @api.onchange('scale_group_id','evaluation')
    def onchange_scale_group_id(self):
        self.ensure_one()
        scale = self.scale_group_id.scale_group_line_ids.filtered(
            lambda l: self.evaluation >= l.eval_start and self.evaluation <= l.eval_end)
        wage = self.scale_group_id.salary
        if(len(scale)==1):
            wage = scale.currency._convert(from_amount=scale.salary,to_currency=self.currency_id)
        self.write({'wage': wage})
    
    