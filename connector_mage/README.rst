.. image:: https://img.shields.io/badge/licence-lgpl--3-blue.svg
   :target: http://www.gnu.org/licenses/LGPL-3.0-standalone.html
   :alt: License: LGPL-3

=================
Connector Magento
=================

This module will link the Magento with Odoo. This is a **POC** for
a very specific requirement without considering much of the security
at application level since the Odoo can be accessible only through
a very specific system. 
It is built on top of the new component based `connector`_ framework.

This will rely on the data source posted from Magento to Odoo, rather
than directly accessing the SOAP API of Magento to reduce load at the
max like 10K order per day.

.. _connector: https://github.com/OCA/connector
.. _connector_ecommerce: https://github.com/OCA/connector-ecommerce
