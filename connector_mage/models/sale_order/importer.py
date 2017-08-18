# -*- coding: utf-8 -*-

from odoo import _
from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.queue_job.exception import FailedJobError, NothingToDoJob


class SaleImportRule(Component):
    _name = 'magento.sale.import.rule'
    _inherit = 'base.magento.connector'
    _apply_on = 'magento.sale.order'
    _usage = 'sale.import.rule'

    def _rule_always(self, record, method):
        return True

    _rules = {'always': _rule_always, }

    def check(self, record):
        payment_method = record['PaymentDetails']
        method = self.env['account.payment.mode'].search(
            [('name', '=', payment_method)],
            limit=1,
        )
        if not method:
            raise FailedJobError(
                "The configuration is missing for the Payment Mode '%s'.\n\n"
                "Resolution:\n"
                "- Go to "
                "'Accounting > Configuration > Management > Payment Modes'\n"
                "- Create a new Payment Mode with name '%s'\n"
                "- Eventually link the Payment Mode to an existing Workflow "
                "Process or create a new one." % (payment_method,
                                                  payment_method))
        self._rules[method.import_rule](self, record, method)


class SaleOrderImportMapper(Component):

    _name = 'magento.sale.order.mapper'
    _inherit = 'magento.import.mapper'
    _apply_on = 'magento.sale.order'

    direct = [
        ('request_id', 'request_id'),
        ('OrderID', 'magento_order_id'),
    ]

    children = [('order_lines', 'magento_order_line_ids', 'magento.sale.order.line'),
                ]

    @mapping
    def name(self, record):
        name = record['OrderID']
        prefix = self.backend_record.sale_prefix
        if prefix:
            name = prefix + name
        return {'name': name}

    @mapping
    def customer_id(self, record):
        binder = self.binder_for('magento.res.partner')
        partner = binder.to_internal(
            record['Customer']['CustomerID'], unwrap=True)
        assert partner, (
            "customer_id %s should have been imported in "
            "SaleOrderImporter._import_dependencies" % record['Customer']['CustomerID'])
        return {'partner_id': partner.id}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def user_id(self, record):
        """ Do not assign to a Salesperson otherwise sales orders are hidden
        for the salespersons (access rules)"""
        return {'user_id': False}


class SaleOrderImporter(Component):
    _name = 'magento.sale.order.importer'
    _inherit = 'magento.importer'
    _apply_on = 'magento.sale.order'

    def _before_import(self):
        rules = self.component(usage='sale.import.rule')
        rules.check(self.magento_record)

    def _build_magento_data(self, post=None):
        order = post['Order']
        lines = order['OrderItems']['OrderItem']
        if isinstance(lines, dict):  # Single line dict, multiple lines list
            lines = [lines]
        order.update({'order_lines': lines})
        return order

    def _must_skip(self):
        if self.binder.to_internal(self.external_id):
            return _('Already imported')

    def _import_dependencies(self):
        record = self.magento_record
        partner = record['Customer']
        partner.update({
            'request_id': record['request_id'],
            'partner_from_order': True,
        })
        importer = self.component(usage='record.importer',
                                  model_name='magento.res.partner')
        importer.run(post=partner)

        lines = record['OrderItems']['OrderItem']
        if isinstance(lines, dict):  # Single line dict, multiple lines list
            lines = [lines]
        for line in lines:
            product_sku = line.pop('Sku')
            line.update({
                'request_id': record['request_id'],
                'product_from_order': True,
                'SKU': product_sku,
            })
            importer = self.component(usage='record.importer',
                                      model_name='magento.product.product')
            importer.run(post=line)

    def run(self, post=None):
        self.magento_record = self._build_magento_data(post=post)
        self.external_id = self.magento_record['OrderID']
        lock_name = 'import({}, {}, {}, {})'.format(
            self.backend_record._name,
            self.backend_record.id,
            self.work.model_name,
            self.external_id,
        )

        skip = self._must_skip()
        if skip:
            return skip

        binding = self._get_binding()

        # Keep a lock on this import until the transaction is committed
        # The lock is kept since we have detected that the informations
        # will be updated into Odoo
        self.advisory_lock_or_retry(lock_name)
        self._before_import()

        self._import_dependencies()

        map_record = self._map_data()

        if binding:
            record = self._update_data(map_record)
            self._update(binding, record)
        else:
            record = self._create_data(map_record)
            binding = self._create(record)

        self.binder.bind(self.magento_record['OrderID'], binding)
        return self._result_message(binding.request_id,
                                    binding.external_id,
                                    binding.odoo_id.id)


class SaleOrderLineImportMapper(Component):

    _name = 'magento.sale.order.line.mapper'
    _inherit = 'magento.import.mapper'
    _apply_on = 'magento.sale.order.line'

    direct = [
        ('Name', 'name'),
        ('Qty', 'product_uom_qty'),
        ('Qty', 'product_qty'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def tax(self, record):
        return {'tax_id': [(4, self.backend_record.default_tax_id.id)]}

    @mapping
    def product_id(self, record):
        binder = self.binder_for('magento.product.product')
        product = binder.to_internal(record['SKU'], unwrap=True)
        assert product, (
            "product_id %s should have been imported in "
            "SaleOrderImporter._import_dependencies" % record['SKU'])
        return {'product_id': product.id}

    @mapping
    def price(self, record):
        return {'price_unit': record['Price']}

    @mapping
    def uom(self, record):
        return {'product_uom': self.backend_record.default_uom_id.id}
