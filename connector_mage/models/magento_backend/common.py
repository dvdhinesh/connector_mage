# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MagentoBackend(models.Model):
    _name = 'magento.backend'
    _description = 'Magento Backend'
    _inherit = 'connector.backend'

    @api.model
    def select_versions(self):
        return [('1.7', '1.7+')]

    version = fields.Selection(selection='select_versions', required=True)
    default_category_id = fields.Many2one(
        comodel_name='product.category',
        string='Default Product Category',
        help='This category will be used for products imported'
             'from Magento.',
    )
    default_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='Default Product UOM',
        help='This UOM will be used for products imported'
             'from Magento.',
    )
    base_backend = fields.Boolean('Base Backend?', defaut=True)
    default_mage_image_url = fields.Char(
        string='Magento Product Image Path',
        required=True,
        help="Url to magento product image path",
    )

    @api.multi
    def product_job_creator(self, post=None):
        backend = self.search([('base_backend', '=', True)])
        self.env['magento.product.product'].with_delay().process_record(
            backend, post=post
        )
        return True

    @api.multi
    def partner_job_creator(self, post=None):
        backend = self.search([('base_backend', '=', True)])
        self.env['magento.res.partner'].with_delay().process_record(
            backend, post=post
        )
        return True
