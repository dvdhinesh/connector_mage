# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MagentoBackend(models.Model):
    _name = 'magento.backend'
    _description = 'Magento Backend'
    _inherit = 'connector.backend'

    base_backend = fields.Boolean('Base Backend?', defaut=True)
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
    default_mage_image_url = fields.Char(
        string='Magento Product Image Path',
        help="Url to magento product image path",
    )
    sale_prefix = fields.Char(
        string='Sale Prefix',
        help="A prefix put before the name of imported sales orders.\n"
             "For instance, if the prefix is 'mag-', the sales "
             "order 100000692 in Magento, will be named 'mag-100000692' "
             "in Odoo.",
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

    @api.multi
    def order_job_creator(self, post=None):
        backend = self.search([('base_backend', '=', True)])
        self.env['magento.sale.order'].with_delay().process_record(
            backend, post=post
        )
        return True
