# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MagentoSaleOrder(models.Model):
    _name = 'magento.sale.order'
    _inherit = 'magento.binding'
    _description = 'Magento Sale Order'
    _inherits = {'sale.order': 'odoo_id'}

    odoo_id = fields.Many2one(comodel_name='sale.order',
                              string='Sale Order',
                              required=True,
                              ondelete='cascade')
    request_id = fields.Char(string="Request ID")
    magento_order_line_ids = fields.One2many(
        comodel_name='magento.sale.order.line',
        inverse_name='magento_order_id',
        string='Magento Order Lines'
    )
    magento_order_id = fields.Char(string='Magento Order ID',
                                      help="'order_id' field in Magento")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    magento_bind_ids = fields.One2many(
        comodel_name='magento.sale.order',
        inverse_name='odoo_id',
        string="Magento Bindings",
    )


class MagentoSaleOrderLine(models.Model):
    _name = 'magento.sale.order.line'
    _inherit = 'magento.binding'
    _description = 'Magento Sale Order Line'
    _inherits = {'sale.order.line': 'odoo_id'}

    magento_order_id = fields.Many2one(comodel_name='magento.sale.order',
                                       string='Magento Sale Order',
                                       required=True,
                                       ondelete='cascade',
                                       index=True)
    odoo_id = fields.Many2one(comodel_name='sale.order.line',
                              string='Sale Order Line',
                              required=True,
                              ondelete='cascade')
    request_id = fields.Char(string="Request ID")

    @api.model
    def create(self, vals):
        magento_order_id = vals['magento_order_id']
        binding = self.env['magento.sale.order'].browse(magento_order_id)
        vals['order_id'] = binding.odoo_id.id
        binding = super(MagentoSaleOrderLine, self).create(vals)
        return binding


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    magento_bind_ids = fields.One2many(
        comodel_name='magento.sale.order.line',
        inverse_name='odoo_id',
        string="Magento Bindings",
    )
