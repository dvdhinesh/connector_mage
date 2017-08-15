# -*- coding: utf-8 -*-

import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class MagentoAPIPost(http.Controller):

    @http.route('/connector-mage-product-post', type='http', auth="public", csrf=False)
    def magento_product_post(self, *args, **post):
        _logger.info('The controller magento_product_post is called.')
        _logger.info(
            '"response": "OK, "args": {0}, "post": {1}'.format(args, post))

        if post:
            Backend = request.env['magento.backend']
            Backend.sudo().product_job_creator(post=post)
        return '"response": "OK", "args": {0}, "post": {1}'.format(args, post)

    @http.route('/connector-mage-customer-post', type='http', auth="public", csrf=False)
    def magento_customer_post(self, *args, **post):
        _logger.info('The controller magento_customer_post is called.')
        _logger.info(
            '"response": "OK, "args": {0}, "post": {1}'.format(args, post))

        if post:
            Backend = request.env['magento.backend']
            Backend.sudo().partner_job_creator(post=post)
        return '"response": "OK", "args": {0}, "post": {1}'.format(args, post)
