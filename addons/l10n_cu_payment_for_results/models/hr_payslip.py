from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    wage = fields.Float("Salario por Evaluación", default=0)
    hw = fields.Float("W/H", default=190.6)
    paid_add = fields.Float("Pago Adicional", default=0)
    paid_value = fields.Float(
        "Pago Adicional Valor", default=0, compute="_compute_paid_value", store=True
    )

    @api.depends("paid_add")
    def _compute_paid_value(self):
        for record in self:
            record.paid_value = record.paid_add / 190.6 * record.hw

    def compute_sheet(self):
        for payslip in self:
            result = payslip.contract_id.wage
            work = self.env["entry.work.adatecssurl"].search(
                [("date", ">=", payslip.date_from), ("date", "<=", payslip.date_to)],
                limit=1,
            )
            line = work.evaluation_line_ids.filtered(
                lambda em, employee=payslip.employee_id: em.employee_id == employee
            )
            if len(line) == 1:
                result = line.wage
                if line.evaluation >= 85 and payslip.paid_add > 0:
                    self.env["hr.payslip.input"].create(
                        {
                            "payslip_id": payslip.id,
                            "amount": f"{payslip.paid_value:.2f}",
                            "contract_id": payslip.contract_id.id,
                            "name": "Aplicación ETT al STR",
                            "code": "ETT-STR",
                            "sequence": len(payslip.input_line_ids),
                        }
                    )
            payslip.write({"wage": result})

            super(HrPayslip, payslip).compute_sheet()
        return True
