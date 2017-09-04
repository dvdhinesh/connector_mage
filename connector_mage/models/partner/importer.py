# -*- coding: utf-8 -*-

import logging

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create
from odoo.addons.queue_job.exception import FailedJobError

_logger = logging.getLogger(__name__)


class PartnerImportMapper(Component):
    _name = 'magento.partner.import.mapper'
    _inherit = 'magento.import.mapper'
    _apply_on = 'magento.res.partner'

    direct = [
        ('request_id', 'request_id'),
        ('Email', 'email'),
        ('Phone', 'phone'),
        ('CompanyName', 'magento_company_name'),
        ('Active', 'magento_active'),
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

    @mapping
    def magento_member_club(self, record):
        if 'ForeignKeyofMemberClub' in record:
            return {'magento_member_club': record['ForeignKeyofMemberClub']}

    @mapping
    def magento_passport_number(self, record):
        if 'NorwayPassportNumber' in record:
            return {'magento_passport_number': record['NorwayPassportNumber']}

    @mapping
    def category_id(self, record):
        existing = self.env['res.partner.category'].search(
            [('magento_customer_type', '=', record['CustomerType'])],
            limit=1,
        )
        if existing:
            return {'category_id': [(6, 0, [existing.id])]}


class PartnerImporter(Component):
    _name = 'magento.partner.importer'
    _inherit = 'magento.importer'
    _apply_on = 'magento.res.partner'

    def _build_magento_data(self, post=None):
        partner = {}
        if 'Customer' in post:
            partner = post['Customer']
            partner.update({'request_id': partner['request_id']})
        elif 'partner_from_order' in post and post['partner_from_order'] == True:
            partner = post
        return partner

    def _after_import(self, partner_binding, magento_record):
        """ Import the addresses """
        invoice_address = {
            'magento_address_name': ' '.join([part for part in (
                magento_record['Name'], magento_record['LastName']
            ) if part]),
            'magento_address': magento_record['Address'],
            'magento_city': magento_record['City'],
            'magento_state': magento_record['State'],
            'magento_state_code': magento_record['StateCode'],
            'magento_zip': magento_record['ZipCode'],
            'magento_country_code': magento_record['CountryCode'],
            'magento_suburb': magento_record['Suburb'],
            'odoo_address_type': 'invoice',
        }
        magento_record.update(invoice_address)
        book = self.component(usage='address.book',
                              model_name='magento.address')
        invoice_address_id = book.import_addresses(
            partner_binding, magento_record)
        if invoice_address_id:
            self.invoice_address_id = invoice_address_id

        if 'partner_from_order' in magento_record and magento_record['partner_from_order'] == True:
            shipping_address = {
                'magento_address_name': ' '.join([part for part in (
                    magento_record['ShippingName'], magento_record['ShippingLastName']
                ) if part]),
                'magento_address': magento_record['ShippingAddress'],
                'magento_city': magento_record['ShippingCity'],
                'magento_state': magento_record['ShippingState'],
                'magento_state_code': magento_record['ShippingStateCode'],
                'magento_zip': magento_record['ShippingZipCode'],
                'magento_country_code': magento_record['ShippingCountryCode'],
                'magento_suburb': magento_record['ShippingSuburb'],
                'odoo_address_type': 'delivery',
            }
            magento_record.update(shipping_address)
            book = self.component(usage='address.book',
                                  model_name='magento.address')
            shipping_address_id = book.import_addresses(
                partner_binding, magento_record)
            if shipping_address_id:
                self.shipping_address_id = shipping_address_id

    def run(self, post=None, expects_address=False):
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
        self._after_import(binding, self.magento_record)
        if expects_address:
            return (self.invoice_address_id, self.shipping_address_id)
        return self._result_message(binding.request_id,
                                    binding.external_id,
                                    binding.odoo_id.id)


class PartnerAddressBook(Component):
    _name = 'magento.address.book'
    _inherit = 'base.magento.connector'
    _apply_on = 'magento.address'
    _usage = 'address.book'

    def import_addresses(self, partner_binding, magento_record):
        odoo_address_type = magento_record['odoo_address_type']
        magento_address_name = magento_record['magento_address_name']
        magento_address = magento_record['magento_address']
        magento_city = magento_record['magento_city']
        magento_state_name = magento_record['magento_state']
        magento_zip = magento_record['magento_zip']
        magento_country_code = magento_record['magento_country_code']
        magento_suburb = magento_record['magento_suburb']
        magento_state = False
        state = False
        country = self.env['res.country'].search(
            [('code', '=', magento_country_code)])
        if magento_state_name:
            # try to find the state in odoo
            state = self.env['res.country.state'].search(
                [('name', '=ilike', magento_state_name)])
            if not state:
                magento_state = magento_state_name  # retain the info from magento
        address = self.env['magento.address'].search(
            [('type', '=', odoo_address_type),
             ('is_company', '=', False),
             ('name', '=', magento_address_name),
             ('street', '=', magento_address),
             ('city', '=', magento_city),
             ('state_id', '=', state.id),
             ('zip', '=', magento_zip),
             ('magento_suburb', '=', magento_suburb),
             ('country_id', '=', country.id)],
            limit=1,
        )
        if not address:
            address = self.env['magento.address'].create({
                'request_id': magento_record['request_id'],
                'backend_id': self.backend_record.id,
                'parent_id': partner_binding.odoo_id.id,
                'type': odoo_address_type,
                'name': magento_address_name,
                'is_company': False,
                'street': magento_address,
                'city': magento_city,
                'state_id': state and state.id or False,
                'magento_state': magento_state,
                'magento_suburb': magento_suburb,
                'zip': magento_zip,
                'country_id': country.id
            })
        return address.odoo_id.id
