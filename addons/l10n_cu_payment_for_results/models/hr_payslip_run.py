from odoo import api, fields, models


class HrPayslipRun(models.Model):
    _inherit = "hr.payslip.run"

    hw = fields.Float("W/H", default=190.6)

    @api.constrains("hw")
    def onchange_hw(self):
        self.ensure_one()
        payslip = self.env["hr.payslip"].search([("payslip_run_id", "=", self.id)])
        for slip in payslip:
            slip.write({"hw": self.hw})
