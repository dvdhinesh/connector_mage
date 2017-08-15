# -*- coding: utf-8 -*-

import logging

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create

_logger = logging.getLogger(__name__)


class PartnerImportMapper(Component):
    _name = 'magento.partner.import.mapper'
    _inherit = 'magento.import.mapper'
    _apply_on = 'magento.res.partner'

    direct = [
        ('request_id', 'request_id'),
        ('Email', 'email'),
    ]

    @only_create
    @mapping
    def is_company(self, record):
        # partners are companies so we can bind
        # addresses on them
        return {'is_company': True}

    @mapping
    def names(self, record):
        parts = [part for part in (record['Name'],
                                   record['LastName']) if part]
        return {'name': ' '.join(parts)}

    @only_create
    @mapping
    def customer(self, record):
        return {'customer': True}

    @mapping
    def type(self, record):
        return {'type': 'contact'}

    @only_create
    @mapping
    def odoo_id(self, record):
        """ Will bind the customer on a existing partner
        with the same email """
        partner = self.env['res.partner'].search(
            [('email', '=', record['Email']),
             ('customer', '=', True),
             '|',
             ('is_company', '=', True),
             ('parent_id', '=', False)],
            limit=1,
        )
        if partner:
            return {'odoo_id': partner.id}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}


class PartnerImporter(Component):
    _name = 'magento.partner.importer'
    _inherit = 'magento.importer'
    _apply_on = 'magento.res.partner'

    def _build_magento_data(self, post=None):
        partner = post['Customer']
        partner.update({'request_id': partner['request_id']})
        return partner

    def run(self, post=None):
        self.magento_record = self._build_magento_data(post=post)
        self.external_id = self.magento_record['CustomerID']
        lock_name = 'import({}, {}, {}, {})'.format(
            self.backend_record._name,
            self.backend_record.id,
            self.work.model_name,
            self.external_id,
        )

        binding = self._get_binding()

        # Keep a lock on this import until the transaction is committed
        # The lock is kept since we have detected that the informations
        # will be updated into Odoo
        self.advisory_lock_or_retry(lock_name)

        map_record = self._map_data()

        if binding:
            record = self._update_data(map_record)
            self._update(binding, record)
        else:
            record = self._create_data(map_record)
            binding = self._create(record)

        self.binder.bind(self.magento_record['CustomerID'], binding)
        return self._result_message(binding.request_id,
                                    binding.external_id,
                                    binding.odoo_id.id)
