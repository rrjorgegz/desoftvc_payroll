# -*- coding: utf-8 -*-
from odoo import models, api, fields


class ResCountryStateMunicipality(models.Model):
    _name = 'res.country.state.municipality'
    _description = "Municipio"
    _order = 'code'
    _rec_name = 'name'

    state_id = fields.Many2one('res.country.state', 'State', required=True)
    name = fields.Char('Nombre del municipio', size=64, required=True)
    code = fields.Char('Código del municipio', size=3,
                       help='El código del municipio en tres caracteres', required=True)
    country_id = fields.Many2one(
        'res.country', related='state_id.country_id', string='País', required=True)
    dpa_code = fields.Char('DPA code', compute='_compute_dpa_code', store=True)

    @api.depends('state_id', 'code')
    def _compute_dpa_code(self):
        for municipality in self:
            if municipality.state_id and municipality.code:
                municipality.dpa_code = '%s%s' % (
                    municipality.state_id.code, municipality.code)

    # @api.model
    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     if args is None:
    #         args = []
    #     if self.env.context.get('state_id'):
    #         args = args + [('state_id', '=', self.env.context.get('state_id'))]
    #     firsts_records = self.search(
    #         [('code', '=ilike', name)] + args, limit=limit)
    #     search_domain = [('name', operator, name)]
    #     search_domain.append(('id', 'not in', firsts_records.ids))
    #     records = firsts_records + \
    #         self.search(search_domain + args, limit=limit)
    #     return [(record.id, record.display_name) for record in records]

    _sql_constraints = [
        ('name_code_uniq', 'unique(state_id, code)',
         'El código del municipio debe ser único!')
    ]
