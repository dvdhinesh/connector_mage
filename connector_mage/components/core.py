# -*- coding: utf-8 -*-

from odoo.addons.component.core import AbstractComponent


class BaseMagentoConnectorComponent(AbstractComponent):
    """ Base Magento Connector Component

    All components of this connector should inherit from it.
    """

    _name = 'base.magento.connector'
    _inherit = 'base.connector'
    _collection = 'magento.backend'
