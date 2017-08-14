# -*- coding: utf-8 -*-

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class ProductImportMapper(Component):
    _name = 'magento.product.product.import.mapper'
    _inherit = 'magento.import.mapper'
    _apply_on = ['magento.product.product']

    direct = [
        ('request_id', 'request_id'),
        ('Name', 'name'),
        ('SKU', 'default_code'),
        ('Description', 'magento_description'),
        ('Lipo', 'is_lipo'),
        ('Watt', 'watt'),
        ('mAh', 'capacity'),
        ('Glue', 'glue'),
        ('Charger', 'charger'),
        ('Airsoft', 'air_soft'),
        ('UnitOfMeasure', 'magento_uom'),
        ('MPQ', 'mpq'),
        ('LengthMm', 'magento_length'),
        ('WidthMm', 'magento_width'),
        ('HeightMm', 'magento_height'),
        ('WeightGrams', 'magento_weight'),
        ('LowSafetyLevel', 'low_safety_level'),
        ('ShowInPO', 'show_in_po'),
        ('ProductImageURL', 'magento_product_image_url'),
        ('ProductURL', 'magento_product_url'),
    ]

    @mapping
    def is_active(self, record):
        return {'active': True}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def type(self, record):
        if record['Type'] == 'simple':
            return {'type': 'product'}

    @mapping
    def categories(self, record):
        return {'categ_id': self.backend_record.default_category_id.id}

    @mapping
    def uom(self, record):
        return {'categ_id': self.backend_record.default_uom_id.id}


class ProductImporter(Component):
    _name = 'magento.product.product.importer'
    _inherit = 'magento.importer'
    _apply_on = ['magento.product.product']

    def _build_magento_data(self, post=None):
        product = post['data']['Product']
        product.pop('Warehouses')
        product.update({'request_id': post['data']['request_id']})
        return product

    def result_message(self, request_id, magent_id, odoo_id):
        return 'Request ID - {0}, Magento ID - {1}, Odoo ID - {2}'.format(request_id,
                                                                          magent_id,
                                                                          odoo_id)

    def run(self, post=None):

        self.magento_record = self._build_magento_data(post=post)

        map_record = self._map_data()

        record = self._create_data(map_record)
        binding = self._create(record)

        self.binder.bind(self.magento_record['ProductID'], binding)
        return self.result_message(binding.request_id,
                                   binding.external_id,
                                   binding.odoo_id.id)