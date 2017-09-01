# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class MagentoProductProduct(models.Model):
    _name = 'magento.product.product'
    _inherit = 'magento.binding'
    _inherits = {'product.product': 'odoo_id'}

    odoo_id = fields.Many2one(comodel_name='product.product',
                              string='Product',
                              required=True,
                              ondelete='restrict')
    request_id = fields.Char(string="Request ID")
    magento_product_id = fields.Char(string="Magento ProductID")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    magento_bind_ids = fields.One2many(
        comodel_name='magento.product.product',
        inverse_name='odoo_id',
        string='Magento Bindings',
    )
    is_lipo = fields.Boolean('Is Lipo?')
    watt = fields.Float()
    capacity = fields.Float('Capacity (mAH)')
    glue = fields.Integer()
    charger = fields.Integer()
    air_soft = fields.Integer('AirSoft')
    magento_uom = fields.Char('UOM on Magento')
    mpq = fields.Float('MPQ')
    magento_length = fields.Float('Length (Mm)')
    magento_width = fields.Float('Width (Mm)')
    magento_height = fields.Float('Height (Mm)')
    magento_weight = fields.Float('Weight (Grams)')
    low_safety_level = fields.Char('Low Safety Level')
    show_in_po = fields.Integer('Show in PO')
    magento_product_image_url = fields.Char('Image URL')
    magento_product_url = fields.Char('Product URL')
    magento_description = fields.Html('Description')
    manuf_sku = fields.Char('Manufacture SKU')
    magento_product_type = fields.Selection([('simple', 'Simple')], default='simple',
                                            string='Product Type')
    hs_category = fields.Char('HSCategory')
    erp_category = fields.Char('ERPCategory')
    magento_attribute_set = fields.Selection([('battery', 'Battery'),
                                              ('motor', 'Motor'),
                                              ('plane', 'Plane'),
                                              ('propeller', 'Propeller'),
                                              ('servo', 'Servo'),
                                              ('others', 'Others')], string='Attribute Set')
    battery_capacity = fields.Char('Capacity')
    battery_discharge = fields.Char('Discharge')
    battery_lengtha = fields.Char('Length A')
    battery_heightb = fields.Char('Height B')
    battery_widthc = fields.Char('Width C')
    battery_unitweight = fields.Char('Unit Weight')
    battery_max_charge_rate = fields.Char('Max Charge Rate')
    battery_watt_hour = fields.Char('Watt Hour')
    battery_config = fields.Char('Config')
    battery_discharge_plug = fields.Char('Discharge Plug')
    battery_islipo = fields.Boolean('Is Lipo?')
    motor_kv = fields.Char('Kv')
    motor_max_current = fields.Char('Max Current')
    motor_powerw = fields.Char('Power W')
    motor_lengthb = fields.Char('Length B')
    motor_can_lengthd = fields.Char('Can Lenght D')
    motor_max_voltage = fields.Char('Max Voltage')
    motor_shafta = fields.Char('Shaft A')
    motor_unit_weight = fields.Char('Unit Weight')
    motor_diameterc = fields.Char('Diameter C')
    motor_total_lengthe = fields.Char('Total Lenght E')
    motor_resistance = fields.Char('Resistance')
    plane_channels = fields.Char('Channels')
    plane_motorsize = fields.Char('Motor Size')
    plane_wingspan = fields.Char('Wing Span')
    plane_lengthmm = fields.Char('Length Mm')
    plane_saleweight = fields.Char('Sale Weight')
    plane_airframe = fields.Char('Airframe')
    plane_frame_pnfrtf = fields.Char('FramePnfRtf')
    plane_ic_elec = fields.Char('IcElec')
    propeller_pitchy = fields.Char('Pitch Y')
    propeller_material = fields.Char('Material')
    propeller_rotation = fields.Char('Rotation')
    propeller_unitweight = fields.Char('Unit Weight')
    propeller_type = fields.Char('Propeller Type')
    propeller_blade_count = fields.Char('Blade Count')
    propeller_diameterx = fields.Char('Diameter X')
    servo_speed = fields.Char('Speed')
    servo_torque = fields.Char('Torque')
    servo_unitweight = fields.Char('Unit Weight')
    servo_amm = fields.Char('A mm')
    servo_bmm = fields.Char('B mm')
    servo_cmm = fields.Char('C mm')
    servo_dmm = fields.Char('D mm')
    servo_emm = fields.Char('E mm')
    servo_fmm = fields.Char('F mm')

    @api.multi
    def magento_product_image(self):
        self.ensure_one()
        backend = self.env['magento.backend'].search(
            [('base_backend', '=', True)])
        if self.magento_product_image_url and backend.default_mage_image_url:
            url = backend.default_mage_image_url + self.magento_product_image_url
        else:
            raise exceptions.UserError('No Image URL specified')
        action = {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url
        }
        return action
