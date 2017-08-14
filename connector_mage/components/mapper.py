# -*- coding: utf-8 -*-

from odoo.addons.component.core import AbstractComponent


class MagentoImportMapper(AbstractComponent):
    _name = 'magento.import.mapper'
    _inherit = ['base.magento.connector', 'base.import.mapper']
    _usage = 'import.mapper'
