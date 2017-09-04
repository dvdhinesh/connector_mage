# -*- coding: utf-8 -*-

import odoo.addons.decimal_precision as dp

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
                                   help="'OrderID' field in XML")
    total_amount = fields.Float(
        string='Total amount',
        digits=dp.get_precision('Account')
    )
    payment_details = fields.Char(string='Payment Details')
    payment_fee = fields.Char(string='Payment Fee')
    paid_date = fields.Datetime(string='Paid Date')
    transation_result = fields.Char(string='Transaction Result')
    magento_customer_ip = fields.Char(string='Magento Customer IP',
                                      help="'CustomerIP' field in XML")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    magento_bind_ids = fields.One2many(
        comodel_name='magento.sale.order',
        inverse_name='odoo_id',
        string="Magento Bindings",
    )
    high_risk_country = fields.Boolean(string='High Risk Country?')
    declared_percentage = fields.Char(string='Declared Percentage')


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
