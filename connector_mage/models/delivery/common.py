# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    magento_code = fields.Char(
        string='Magento Carrier Code',
        required=False,
    )
    magento_export_tracking = fields.Boolean(string='Export tracking numbers',
                                             default=True)
