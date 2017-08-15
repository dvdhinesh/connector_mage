# -*- coding: utf-8 -*-

from odoo.addons.component.core import Component


class MagentoModelBinder(Component):
    _name = 'magento.binder'
    _inherit = ['base.binder', 'base.magento.connector']
    _apply_on = [
        'magento.res.partner',
        'magento.product.product',
    ]
