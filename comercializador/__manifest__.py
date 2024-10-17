# -*- coding: utf-8 -*-
{
    'name': "Comercializador EnerguX",
    'summary':"""
        Gestión del comercio del producto Energux
    """,
    'author':'Adonnis Almeida Montesino (adonnis.almeida@desoft.cu)',
    'category':'Comercializador',
    'sequence': -100,
    'version':'1.0.0',
    'application': True,
    'depends':[],
    'data':[
        'security/comercializador_security.xml',
        'security/ir.model.access.csv',
        'wizard/importar_ventas_wizard.xml',
        'wizard/procesar_ventas_wizard.xml',
        'wizard/generar_licencia_wizard.xml',
        'views/menu_view.xml',
        'views/division_view.xml',
        'views/producto_view.xml',
        'views/cliente_view.xml',
        'views/venta_view.xml',
        'views/licencia_view.xml',
        'views/historial_licencia_view.xml',
        'views/assets.xml',
    ],
    'qweb': [
        "static/src/xml/tree_button.xml",
    ],
} # type: ignore