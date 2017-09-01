# -*- coding: utf-8 -*-

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


MAGENTO_ATTRIBUTE_SET = {
    'Battery': 'battery',
    'Motor': 'motor',
    'Plane': 'plane',
    'Propeller': 'propeller',
    'Servo': 'servo',
    'Others': 'others',
}


class ProductImportMapper(Component):
    _name = 'magento.product.product.import.mapper'
    _inherit = 'magento.import.mapper'
    _apply_on = ['magento.product.product']

    direct = [
        ('request_id', 'request_id'),
        ('Name', 'name'),
        ('SKU', 'default_code'),
        ('Description', 'magento_description'),
        ('Lipo', 'is_lipo'),
        ('Watt', 'watt'),
        ('mAh', 'capacity'),
        ('Glue', 'glue'),
        ('Charger', 'charger'),
        ('Airsoft', 'air_soft'),
        ('UnitOfMeasure', 'magento_uom'),
        ('MPQ', 'mpq'),
        ('LengthMm', 'magento_length'),
        ('WidthMm', 'magento_width'),
        ('HeightMm', 'magento_height'),
        ('WeightGrams', 'magento_weight'),
        ('LowSafetyLevel', 'low_safety_level'),
        ('ShowInPO', 'show_in_po'),
        ('ProductImageURL', 'magento_product_image_url'),
        ('ProductURL', 'magento_product_url'),
        ('ManufSKU', 'manuf_sku'),
        ('Type', 'magento_product_type'),
        ('HSCategory', 'hs_category'),
        ('ERPCategory', 'erp_category'),
    ]

    @mapping
    def is_active(self, record):
        return {'active': True}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def type(self, record):
        return {'type': 'product'}

    @mapping
    def categories(self, record):
        return {'categ_id': self.backend_record.default_category_id.id}

    @mapping
    def uom(self, record):
        return {'categ_id': self.backend_record.default_uom_id.id}

    @mapping
    def magento_product_id(self, record):
        if 'ProductID' in record:
            return {'magento_product_id': record['ProductID']}

    @mapping
    def attribute_set(self, record):
        return {'magento_attribute_set':
                MAGENTO_ATTRIBUTE_SET.get(record['AttributeSet'], False)}

    @mapping
    def battery_capacity(self, record):
        if record['AttributeSet'] == 'Battery':
            return {'battery_capacity': record['Attributes']['Capacity']}

    @mapping
    def battery_discharge(self, record):
        if record['AttributeSet'] == 'Battery':
            return {'battery_discharge': record['Attributes']['Discharge']}

    @mapping
    def battery_heightb(self, record):
        if record['AttributeSet'] == 'Battery':
            return {'battery_heightb': record['Attributes']['HeightB']}

    @mapping
    def battery_widthc(self, record):
        if record['AttributeSet'] == 'Battery':
            return {'battery_widthc': record['Attributes']['WidthC']}

    @mapping
    def battery_unitweight(self, record):
        if record['AttributeSet'] == 'Battery':
            return {'battery_unitweight': record['Attributes']['UnitWeight']}

    @mapping
    def battery_max_charge_rate(self, record):
        if record['AttributeSet'] == 'Battery':
            return {'battery_max_charge_rate': record['Attributes']['MaxChargeRate']}

    @mapping
    def battery_watt_hour(self, record):
        if record['AttributeSet'] == 'Battery':
            return {'battery_watt_hour': record['Attributes']['WattHour']}

    @mapping
    def battery_config(self, record):
        if record['AttributeSet'] == 'Battery':
            return {'battery_config': record['Attributes']['Config']}

    @mapping
    def battery_discharge_plug(self, record):
        if record['AttributeSet'] == 'Battery':
            return {'battery_discharge_plug': record['Attributes']['DischargePlug']}

    @mapping
    def battery_islipo(self, record):
        if record['AttributeSet'] == 'Battery' and record['Attributes']['IsLipo'] == 'Yes':
            return {'battery_islipo': 1}

    @mapping
    def motor_kv(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_kv': record['Attributes']['Kv']}

    @mapping
    def motor_max_current(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_max_current': record['Attributes']['MaxCurrent']}

    @mapping
    def motor_powerw(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_powerw': record['Attributes']['PowerW']}

    @mapping
    def motor_lengthb(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_lengthb': record['Attributes']['LengthB']}

    @mapping
    def motor_can_lengthd(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_can_lengthd': record['Attributes']['CanLenghtD']}

    @mapping
    def motor_max_voltage(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_max_voltage': record['Attributes']['MaxVoltage']}

    @mapping
    def motor_shafta(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_shafta': record['Attributes']['ShaftA']}

    @mapping
    def motor_unit_weight(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_unit_weight': record['Attributes']['UnitWeight']}

    @mapping
    def motor_diameterc(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_diameterc': record['Attributes']['DiameterC']}

    @mapping
    def motor_total_lengthe(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_total_lengthe': record['Attributes']['TotalLenghtE']}

    @mapping
    def motor_resistance(self, record):
        if record['AttributeSet'] == 'Motor':
            return {'motor_resistance': record['Attributes']['Resistance']}

    @mapping
    def plane_channels(self, record):
        if record['AttributeSet'] == 'Plane':
            return {'plane_channels': record['Attributes']['Channels']}

    @mapping
    def plane_motorsize(self, record):
        if record['AttributeSet'] == 'Plane':
            return {'plane_motorsize': record['Attributes']['Motorsize']}

    @mapping
    def plane_wingspan(self, record):
        if record['AttributeSet'] == 'Plane':
            return {'plane_wingspan': record['Attributes']['Wingspan']}

    @mapping
    def plane_lengthmm(self, record):
        if record['AttributeSet'] == 'Plane':
            return {'plane_lengthmm': record['Attributes']['LengthMm']}

    @mapping
    def plane_saleweight(self, record):
        if record['AttributeSet'] == 'Plane':
            return {'plane_saleweight': record['Attributes']['SaleWeight']}

    @mapping
    def plane_airframe(self, record):
        if record['AttributeSet'] == 'Plane':
            return {'plane_airframe': record['Attributes']['Airframe']}

    @mapping
    def plane_frame_pnfrtf(self, record):
        if record['AttributeSet'] == 'Plane':
            return {'plane_frame_pnfrtf': record['Attributes']['FramePnfRtf']}

    @mapping
    def plane_ic_elec(self, record):
        if record['AttributeSet'] == 'Plane':
            return {'plane_ic_elec': record['Attributes']['IcElec']}

    @mapping
    def propeller_pitchy(self, record):
        if record['AttributeSet'] == 'Propeller':
            return {'propeller_pitchy': record['Attributes']['PitchY']}

    @mapping
    def propeller_material(self, record):
        if record['AttributeSet'] == 'Propeller':
            return {'propeller_material': record['Attributes']['Material']}

    @mapping
    def propeller_rotation(self, record):
        if record['AttributeSet'] == 'Propeller':
            return {'propeller_rotation': record['Attributes']['Rotation']}

    @mapping
    def propeller_unitweight(self, record):
        if record['AttributeSet'] == 'Propeller':
            return {'propeller_unitweight': record['Attributes']['UnitWeight']}

    @mapping
    def propeller_type(self, record):
        if record['AttributeSet'] == 'Propeller':
            return {'propeller_type': record['Attributes']['PropellerType']}

    @mapping
    def propeller_blade_count(self, record):
        if record['AttributeSet'] == 'Propeller':
            return {'propeller_blade_count': record['Attributes']['BladeCount']}

    @mapping
    def propeller_diameterx(self, record):
        if record['AttributeSet'] == 'Propeller':
            return {'propeller_diameterx': record['Attributes']['DiameterX']}

    @mapping
    def servo_speed(self, record):
        if record['AttributeSet'] == 'Servo':
            return {'servo_speed': record['Attributes']['Speed']}

    @mapping
    def servo_torque(self, record):
        if record['AttributeSet'] == 'Servo':
            return {'servo_torque': record['Attributes']['Torque']}

    @mapping
    def servo_unitweight(self, record):
        if record['AttributeSet'] == 'Servo':
            return {'servo_unitweight': record['Attributes']['UnitWeight']}

    @mapping
    def servo_amm(self, record):
        if record['AttributeSet'] == 'Servo':
            return {'servo_amm': record['Attributes']['Amm']}

    @mapping
    def servo_bmm(self, record):
        if record['AttributeSet'] == 'Servo':
            return {'servo_bmm': record['Attributes']['Bmm']}

    @mapping
    def servo_cmm(self, record):
        if record['AttributeSet'] == 'Servo':
            return {'servo_cmm': record['Attributes']['Cmm']}

    @mapping
    def servo_dmm(self, record):
        if record['AttributeSet'] == 'Servo':
            return {'servo_dmm': record['Attributes']['Dmm']}

    @mapping
    def servo_emm(self, record):
        if record['AttributeSet'] == 'Servo':
            return {'servo_emm': record['Attributes']['Emm']}

    @mapping
    def servo_fmm(self, record):
        if record['AttributeSet'] == 'Servo':
            return {'servo_fmm': record['Attributes']['Fmm']}


class ProductImporter(Component):
    _name = 'magento.product.product.importer'
    _inherit = 'magento.importer'
    _apply_on = ['magento.product.product']

    def _build_magento_data(self, post=None):
        product = {}
        if 'data' in post:
            product = post['data']['Product']
            product.pop('Warehouses')
            product.update({'request_id': post['data']['request_id']})
        elif 'product_from_order' in post and post['product_from_order'] == True:
            product = post
        return product

    def run(self, post=None):
        self.magento_record = self._build_magento_data(post=post)
        self.external_id = self.magento_record['SKU']
        lock_name = 'import({}, {}, {}, {})'.format(
            self.backend_record._name,
            self.backend_record.id,
            self.work.model_name,
            self.external_id,
        )

        binding = self._get_binding()

        # Keep a lock on this import until the transaction is committed
        # The lock is kept since we have detected that the informations
        # will be updated into Odoo
        self.advisory_lock_or_retry(lock_name)

        map_record = self._map_data()

        if binding:
            record = self._update_data(map_record)
            self._update(binding, record)
        else:
            record = self._create_data(map_record)
            binding = self._create(record)

        self.binder.bind(self.magento_record['SKU'], binding)
        return self._result_message(binding.request_id,
                                    binding.external_id,
                                    binding.odoo_id.id)
