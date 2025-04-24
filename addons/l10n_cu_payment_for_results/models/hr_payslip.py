from odoo import fields, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    wage = fields.Float("Salario por Evaluación", default=0)
    hw = fields.Float("W/H", default=190.6)

    def compute_sheet(self):
        for payslip in self:
            result = payslip.contract_id.wage
            work = self.env["entry.work.adatecssurl"].search(
                [("date", ">=", payslip.date_from), ("date", "<=", payslip.date_to)],
                limit=1,
            )
            employee_id = work.evaluation_line_ids.mapped("employee_id")
            line = employee_id.filtered(payslip.employee_id)
            if len(line) == 1:
                result = line.wage
            payslip.write({"wage": result})

            super(HrPayslip, payslip).compute_sheet()
        return True
