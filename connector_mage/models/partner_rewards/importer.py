# -*- coding: utf-8 -*-

from datetime import datetime
import logging

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create
from odoo.addons.queue_job.exception import RetryableJobError, NothingToDoJob

_logger = logging.getLogger(__name__)


class RewardsImportRule(Component):
    _name = 'magento.partner.rewards.import.rule'
    _inherit = 'base.magento.connector'
    _apply_on = 'magento.res.partner.rewards'
    _usage = 'rewards.import.rule'

    def check(self, record):
        # cannot import this as a dependency since the data source was posted, not imported
        partner_binder = self.binder_for('magento.res.partner')
        partner_binding = partner_binder.to_internal(record['CustomerID'])
        if not partner_binding:
            raise RetryableJobError(
                "Couldn't find respective Customer ID - %s "
                "for the Request ID - %s" % (record['CustomerID'],
                                             record['request_id']), seconds=1 * 60)
        rewards_binder = self.binder_for('magento.res.partner.rewards')
        rewards_binding = rewards_binder.to_internal(record['CustomerID'])
        if rewards_binding:
            existing_date = datetime.strptime(
                rewards_binding.magento_date_modified, '%Y-%m-%d %H:%M:%S')
            modified_dt = datetime.strptime(
                record['ModifiedDate'], '%Y-%m-%d %H:%M:%S')
            if modified_dt < existing_date:
                raise NothingToDoJob(
                    "The most recent rewards point already imported with this Request ID - %s.\n"
                    "This is old Request ID - %s. Odoo ID - %s" % (rewards_binding.request_id,
                                                                   record['request_id'],
                                                                   rewards_binding.odoo_id.id))


class PartnerRewardsImportMapper(Component):
    _name = 'magento.partner.rewards.import.mapper'
    _inherit = 'magento.import.mapper'
    _apply_on = 'magento.res.partner.rewards'

    direct = [
        ('request_id', 'request_id'),
        ('RewardPoint', 'magento_rewards_point'),
        ('StoreCredit', 'magento_store_credit'),
        ('ModifiedDate', 'magento_date_modified'),
    ]

    @only_create
    @mapping
    def odoo_id(self, record):
        partner = self.env['magento.res.partner'].search(
            [('external_id', '=', record['CustomerID'])],
            limit=1,
        )
        if partner:
            return {'odoo_id': partner.odoo_id.id}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}


class PartnerRewardsImporter(Component):
    _name = 'magento.partner.rewards.importer'
    _inherit = 'magento.importer'
    _apply_on = 'magento.res.partner.rewards'

    def _build_magento_data(self, post=None):
        record = {}
        if 'Customer' in post:
            record = post['Customer']
        return record

    def _before_import(self):
        rules = self.component(usage='rewards.import.rule')
        rules.check(self.magento_record)

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
        self._before_import()

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
