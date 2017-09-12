# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    magento_rewards_bind_ids = fields.One2many(
        comodel_name='magento.res.partner.rewards',
        inverse_name='odoo_id',
        string="Magento Bindings",
    )
    magento_rewards_point = fields.Float(string="Magento Rewards Point")
    magento_store_credit = fields.Float(string="Magento Store Credit")


class MagentoResPartnerRewards(models.Model):
    _name = 'magento.res.partner.rewards'
    _inherit = 'magento.binding'
    _inherits = {'res.partner': 'odoo_id'}
    _description = 'Magento Partner Rewards'

    _rec_name = 'name'

    odoo_id = fields.Many2one(comodel_name='res.partner',
                              string='Partner',
                              required=True,
                              ondelete='cascade')
    request_id = fields.Char(string="Request ID")
    magento_date_modified = fields.Char(
        string="Magento Modified Date")  # keep it char, don't handle tz
