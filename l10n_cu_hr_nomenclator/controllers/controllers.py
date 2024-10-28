# -*- coding: utf-8 -*-
# from odoo import http


# class L10nCuHrNomenclator(http.Controller):
#     @http.route('/l10n_cu_hr_nomenclator/l10n_cu_hr_nomenclator', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_cu_hr_nomenclator/l10n_cu_hr_nomenclator/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_cu_hr_nomenclator.listing', {
#             'root': '/l10n_cu_hr_nomenclator/l10n_cu_hr_nomenclator',
#             'objects': http.request.env['l10n_cu_hr_nomenclator.l10n_cu_hr_nomenclator'].search([]),
#         })

#     @http.route('/l10n_cu_hr_nomenclator/l10n_cu_hr_nomenclator/objects/<model("l10n_cu_hr_nomenclator.l10n_cu_hr_nomenclator"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_cu_hr_nomenclator.object', {
#             'object': obj
#         })

