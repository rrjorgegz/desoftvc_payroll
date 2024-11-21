# -*- coding: utf-8 -*-
{
    'name': "PAGO POR RESULTADOS",

    'summary': "UEB DESOFT VILLA CLARA",

    'description': """
PAGO POR RESULTADOS PARA LA UEB DESOFT VILLA CLARA (ADATECSsurl)
    """,

    'author': "UEB DESOFT VILLA CLARA (ADATECSsurl)",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Payment for results',
    'version': '0.1',
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    'depends': ['l10n_cu_hr_nomenclator', 'hr_payroll_holidays'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'wizard/generate_evaluation_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_payslip_run_views.xml',
        'views/entry_work_adatecssurl_views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

