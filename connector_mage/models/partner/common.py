# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    magento_bind_ids = fields.One2many(
        comodel_name='magento.res.partner',
        inverse_name='odoo_id',
        string="Magento Bindings",
    )


class MagentoResPartner(models.Model):
    _name = 'magento.res.partner'
    _inherit = 'magento.binding'
    _inherits = {'res.partner': 'odoo_id'}
    _description = 'Magento Partner'

    _rec_name = 'name'

    odoo_id = fields.Many2one(comodel_name='res.partner',
                              string='Partner',
                              required=True,
                              ondelete='cascade')
    request_id = fields.Char(string="Request ID")
