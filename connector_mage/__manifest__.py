# -*- coding: utf-8 -*-

{
    'name': 'Magento Connector',
    'version': '10.0.1.0.0',
    'author': 'Dhinesh D',
    'category': 'Connector',
    'depends': [
                'product',
                'delivery',
                'sale_stock',
                'connector_ecommerce',
    ],
    'external_dependencies': {
        'python': ['xmltodict'],
    },
    'data': [
        'views/magento_backend_views.xml',
        'views/product_views.xml',
        'views/partner_views.xml',
        'views/delivery_views.xml',
        'views/sale_order_views.xml',
        'views/connector_magento_menu.xml',
    ],
    'installable': True,
    'application': True,
}
