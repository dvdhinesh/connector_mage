# -*- coding: utf-8 -*-

"""

Importers for Magento.

An import can be skipped if the last sync date is more recent than
the last update in Magento.

They should call the ``bind`` method if the binder even if the records
are already bound, to update the last sync date.

"""

import logging
from odoo import fields, _
from odoo.addons.component.core import AbstractComponent, Component
from odoo.addons.connector.exception import IDMissingInBackend
from odoo.addons.queue_job.exception import NothingToDoJob

_logger = logging.getLogger(__name__)


class MagentoImporter(AbstractComponent):
    """ Base importer for Magento """

    _name = 'magento.importer'
    _inherit = ['base.importer', 'base.magento.connector']
    _usage = 'record.importer'

    def __init__(self, work_context):
        super(MagentoImporter, self).__init__(work_context)
        self.external_id = None
        self.magento_record = None

    def _before_import(self):
        return

    def _is_uptodate(self, binding):
        return

    def _import_dependency(self, external_id, binding_model,
                           importer=None, always=False):
        return

    def _import_dependencies(self):
        return

    def _map_data(self):
        return self.mapper.map_record(self.magento_record)

    def _validate_data(self, data):
        return

    def _must_skip(self):
        return

    def _get_binding(self):
        return self.binder.to_internal(self.external_id)

    def _create_data(self, map_record, **kwargs):
        return map_record.values(for_create=True, **kwargs)

    def _create(self, data):
        """ Create the OpenERP record """
        # special check on data before import
        self._validate_data(data)
        model = self.model.with_context(connector_no_export=True)
        binding = model.create(data)
        _logger.debug('%d created from magento %s', binding, self.external_id)
        return binding

    def _update_data(self, map_record, **kwargs):
        return map_record.values(**kwargs)

    def _update(self, binding, data):
        """ Update an OpenERP record """
        # special check on data before import
        self._validate_data(data)
        binding.with_context(connector_no_export=True).write(data)
        _logger.debug('%d updated from magento %s', binding, self.external_id)
        return

    def _after_import(self, binding):
        return

    def _result_message(self, request_id, magent_id, odoo_id):
        return 'Request ID - {0}, Magento ID - {1}, Odoo ID - {2}'.format(request_id,
                                                                          magent_id,
                                                                          odoo_id)

    def run(self, external_id, force=False):
        return
