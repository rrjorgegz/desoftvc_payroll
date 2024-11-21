from datetime import datetime
from odoo import models, fields, api, _


class GenerateEvaluation(models.TransientModel):
    _name = "generate.evaluation"
    _description = "Generar Evaluación"
    
    entry_work_id = fields.Many2one( 'entry.work.adatecssurl',required=True)
    employee_ids = fields.Many2many('hr.employee', string="Empleados")
    date = fields.Date(string='Fecha', required=True, default=datetime.today())
    
    def generate_evaluation(self):
        self.ensure_one()
        line = self.entry_work_id.evaluation_line_ids
        line.unlink()
        for employee in self.employee_ids:
            contract = False
            scale_group = False
            wage = 0
            currency_id = self.env.ref('base.CUP')
            data = self.env['hr.contract'].search(
                [('employee_id', '=', employee.id), ('active', '=', True)], limit=1)
            if len(data) > 0:
                contract = data[0].id
                scale_group = data[0].scale_group.id
                scale = data[0].scale_group.scale_group_line_ids.filtered(
                lambda l: 85 >= l.eval_start and 85 <= l.eval_end)
                wage = data[0].scale_group.currency._convert(
                    from_amount=data[0].scale_group.salary, to_currency=data[0].currency_id)
                currency_id = data[0].currency_id
            line.create({
                'evaluation': 85, 
                'employee_id': employee.id,
                'contract_id': contract,
                'scale_group_id': scale_group,
                'wage': wage,
                'currency_id': currency_id.id,
            })
        #     self
        return
