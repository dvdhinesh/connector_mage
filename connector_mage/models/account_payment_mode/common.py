# -*- coding: utf-8 -*-

from odoo import models, api


class AccountPaymentMode(models.Model):
    _inherit = "account.payment.mode"

    @api.model
    def _get_import_rules(self):
        return [('always', 'Always'), ]
