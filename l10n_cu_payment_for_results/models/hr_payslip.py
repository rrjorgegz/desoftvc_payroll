from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class HrPayslip(models.Model):
    _inherit = "hr.payslip"
    
    wage = fields.Float('Salario por Evaluación',default=0) 
    hw = fields.Float('W/H', default=190.6)
         
    def compute_sheet(self):
        for payslip in self:
            result = payslip.contract_id.wage
            work = self.env['entry.work.adatecssurl'].search(
                [('date', '>=', payslip.date_from), ('date', '<=', payslip.date_to)], limit=1)
            line = work.evaluation_line_ids.filtered(
                lambda l: l.employee_id == payslip.employee_id)
            if len(line)==1:
                result = line.wage
            payslip.write({'wage': result})
            
            super(HrPayslip, payslip).compute_sheet()
        return True 
        