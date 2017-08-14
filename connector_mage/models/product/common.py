# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class MagentoProductProduct(models.Model):
    _name = 'magento.product.product'
    _inherit = 'magento.binding'
    _inherits = {'product.product': 'odoo_id'}

    odoo_id = fields.Many2one(comodel_name='product.product',
                              string='Product',
                              required=True,
                              ondelete='restrict')
    request_id = fields.Char(string="Request ID")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    magento_bind_ids = fields.One2many(
        comodel_name='magento.product.product',
        inverse_name='odoo_id',
        string='Magento Bindings',
    )
    is_lipo = fields.Boolean('Is Lipo?')
    watt = fields.Float()
    capacity = fields.Float('Capacity (mAH)')
    glue = fields.Integer()
    charger = fields.Integer()
    air_soft = fields.Integer('AirSoft')
    magento_uom = fields.Char('UOM on Magento')
    mpq = fields.Float('MPQ')
    magento_length = fields.Float('Length (Mm)')
    magento_width = fields.Float('Width (Mm)')
    magento_height = fields.Float('Height (Mm)')
    magento_weight = fields.Float('Weight (Grams)')
    low_safety_level = fields.Char('Low Safety Level')
    show_in_po = fields.Integer('Show in PO')
    magento_product_image_url = fields.Char('Image URL')
    magento_product_url = fields.Char('Product URL')
    magento_description = fields.Html('Description')

    @api.multi
    def magento_product_image(self):
        self.ensure_one()
        backend = self.env['magento.backend'].search(
            [('base_backend', '=', True)])
        if self.magento_product_image_url and backend.default_mage_image_url:
            url = backend.default_mage_image_url + self.magento_product_image_url
        else:
            raise exceptions.UserError('No Image URL specified')
        action = {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url
        }
        return action
