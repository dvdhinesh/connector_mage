# -*- coding: utf-8 -*-

from odoo.addons.component.core import AbstractComponent


class MagentoImportMapper(AbstractComponent):
    _name = 'magento.import.mapper'
    _inherit = ['base.magento.connector', 'base.import.mapper']
    _usage = 'import.mapper'


def normalize_datetime(field):
    """Change a invalid date which comes from Magento, if
    no real date is set to null for correct import to
    OpenERP"""

    def modifier(self, record, to_attr):
        if record[field] == '0000-00-00 00:00:00':
            return None
        return record[field]
    return modifier
