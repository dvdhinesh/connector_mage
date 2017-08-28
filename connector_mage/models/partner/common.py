# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    magento_bind_ids = fields.One2many(
        comodel_name='magento.res.partner',
        inverse_name='odoo_id',
        string="Magento Bindings",
    )
    magento_address_bind_ids = fields.One2many(
        comodel_name='magento.address',
        inverse_name='odoo_id',
        string="Magento Address Bindings",
    )
    magento_state = fields.Char(string='Magento State')
    magento_company_name = fields.Char(string='Magento Company Name')


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


class MagentoAddress(models.Model):
    _name = 'magento.address'
    _inherit = 'magento.binding'
    _inherits = {'res.partner': 'odoo_id'}
    _description = 'Magento Address'

    _rec_name = 'backend_id'

    odoo_id = fields.Many2one(comodel_name='res.partner',
                              string='Partner',
                              required=True,
                              ondelete='cascade')
    request_id = fields.Char(string="Request ID")
