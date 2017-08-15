# -*- coding: utf-8 -*-

import xmltodict

from odoo import api, models, fields
from odoo.addons.queue_job.job import job, related_action
from odoo.addons.queue_job.exception import JobError


def xml_to_dict(xml):
    value = "%s" % xml.values()[0]
    return xmltodict.parse(value)


class MagentoBinding(models.AbstractModel):
    _name = 'magento.binding'
    _inherit = 'external.binding'
    _description = 'Magento Binding (abstract)'

    backend_id = fields.Many2one(
        comodel_name='magento.backend',
        string='Magento Backend',
        required=True,
        ondelete='restrict',
    )
    external_id = fields.Char(string='ID on Magento')

    _sql_constraints = [
        ('magento_uniq', 'unique(backend_id, external_id)',
         'A binding already exists with the same Magento ID.'),
    ]

    @job(default_channel='root.magento')
    @related_action(action='related_action_from_result')
    @api.model
    def process_record(self, backend, post=None):
        """ Process a Magento record """
        try:
            post_dict = xml_to_dict(post)
        except Exception, e:
            raise JobError(e)

        with backend.work_on(self._name) as work:
            importer = work.component(usage='record.importer')
            return importer.run(post=post_dict)
