# -*- coding: utf-8 -*-
# from odoo import http


# class L10nCuPaymentForResults(http.Controller):
#     @http.route('/l10n_cu_payment_for_results/l10n_cu_payment_for_results', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_cu_payment_for_results/l10n_cu_payment_for_results/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_cu_payment_for_results.listing', {
#             'root': '/l10n_cu_payment_for_results/l10n_cu_payment_for_results',
#             'objects': http.request.env['l10n_cu_payment_for_results.l10n_cu_payment_for_results'].search([]),
#         })

#     @http.route('/l10n_cu_payment_for_results/l10n_cu_payment_for_results/objects/<model("l10n_cu_payment_for_results.l10n_cu_payment_for_results"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_cu_payment_for_results.object', {
#             'object': obj
#         })

