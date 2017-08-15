# -*- coding: utf-8 -*-

from odoo import api, models


MODEL_MAPPING = {
    'magento.product.product': 'product.product',
    'magento.res.partner': 'res.partner'
}


class QueueJob(models.Model):

    _inherit = 'queue.job'

    @api.multi
    def related_action_from_result(self):
        self.ensure_one()
        if self.result and MODEL_MAPPING.get(self.model_name, False):
            model = MODEL_MAPPING[self.model_name]
            record_id = self.result.split()[-1]
            action = {
                'name': "Related Record",
                'type': 'ir.actions.act_window',
                'res_model': model,
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': int(record_id),
            }
            return action
