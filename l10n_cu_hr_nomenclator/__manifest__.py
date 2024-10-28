# -*- coding: utf-8 -*-
{
    'name': "NOMENCLADORES",

    'summary': "UEB DESOFT VILLA CLARA",

    'description': """
NOMENCLADORES PARA LA UEB DESOFT VILLA CLARA (ADATECSsurl)
    """,

    'author': "UEB DESOFT VILLA CLARA (ADATECSsurl)",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Nomenclator',
    'version': '0.1',
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    'depends': ['hr_skills', 'contacts'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/classification_retired_workers_data.xml',
        'data/disciplinary_measures_data.xml',
        'data/hr_category_data.xml',
        'data/hr_rejects_data.xml',
        'data/necesary_docs_data.xml',
        'data/nivel_certificado_data.xml',
        'data/org_military_data.xml',
        'data/org_politics_data.xml',
        'data/org_populations_data.xml',
        'data/res_state_municipality_data.xml',
        'data/scale_group_data.xml',
        'data/resource_calendar_data.xml',
        'data/hr_department_data.xml',
        'data/hr_employee_data.xml',
        'data/hr_contract_data.xml',        
        'views/menu_root_views.xml',
        'views/campo_estudio_views.xml',
        'views/causa_baja_views.xml',
        'views/classification_retired_workers_views.xml',
        'views/disciplinary_measured_types_views.xml',
        'views/disciplinary_measures_views.xml',
        'views/hr_category_views.xml',
        'views/hr_department_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_job_views.xml',
        'views/hr_rejects_views.xml',
        'views/necesary_docs_views.xml',
        'views/nivel_certificado_views.xml',
        'views/org_military_views.xml',
        'views/org_politics_views.xml',
        'views/org_populations_views.xml',
        'views/res_country_state_municipality_views.xml',
        'views/res_partner_views.xml',
        'views/scale_group_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

