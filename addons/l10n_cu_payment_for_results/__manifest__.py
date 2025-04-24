{
    "name": "PAGO POR RESULTADOS",
    "summary": "PAGO POR RESULTADOS PARA LA UEB DESOFT VILLA CLARA (ADATECSsurl)",
    "author": "ADATECS.surl",
    "website": "https://www.desoft.cu",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Human Resources/Payment for results",
    "version": "17.0.0.0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": ["l10n_cu_hr_nomenclator", "hr_payroll_holidays"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "wizard/generate_evaluation_views.xml",
        "views/hr_payslip_views.xml",
        "views/hr_payslip_run_views.xml",
        "views/entry_work_adatecssurl_views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        # 'demo/demo.xml',
    ],
}
