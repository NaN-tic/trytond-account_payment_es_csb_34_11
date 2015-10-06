## coding: utf-8
# This file is part of account_payment_es_csb_34_11 module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.pyson import Eval
import logging

try:
    from retrofix import Record, write, c34_11
except ImportError:
    logger = logging.getLogger(__name__)
    message = ('Unable to import retrofix library.\n'
               'Please install it before install this module.')
    logger.error(message)
    raise Exception(message)

__all__ = [
    'Journal',
    'Group',
    ]
__metaclass__ = PoolMeta


class Journal:
    __name__ = 'account.payment.journal'

    @classmethod
    def __setup__(cls):
        super(Journal, cls).__setup__()
        if ('csb34_11', 'CSB 34-11') not in cls.process_method.selection:
            cls.process_method.selection.extend([
                ('csb34_11', 'CSB 34-11'),
                ])

    @classmethod
    def view_attributes(cls):
        return super(Journal, cls).view_attributes() + [
            ('//group[@id="csb_34_1"]', 'states', {
                    'invisible': Eval('process_method') != 'csb34_11',
                    }),
            ('//group[@id="csb_34_1"]/group[@id="csb_34_type"]', 'states', {
                    'invisible': Eval('csb34_type') == 'transfer',
                    }),
            ('//group[@id="csb_34_1"]/group[@id="csb_34_type"]/group[@id="csb_34_other"]', 'states', {
                    'invisible': Eval('send_type') == 'other',
                    })]


class Group:
    __name__ = 'account.payment.group'

    def set_default_csb34_11_payment_values(self):
        values = self.set_default_csb34_payment_values()
        return values

    @classmethod
    def process_csb34_11(cls, group):
        def set_ordering_header_record():
            record = Record(c34_11.ORDERING_HEADER_RECORD)
            record.record_code = '03'
            record.data_code = '62'
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.data_number = '001'
            record.send_date = values['payment_date']
            record.creation_date = values['creation_date']
            record.account = values['bank_account']
            record.charge_detail = 'false'  # or 'true'
            return write([record])

        def set_ordering_header_002_record():
            record = Record(c34_11.ORDERING_HEADER_002_RECORD)
            record.record_code = '03'
            record.data_code = '62'
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.data_number = '002'
            record.name = values['party'].name
            return write([record])

        def set_ordering_header_003_record():
            record = Record(c34_11.ORDERING_HEADER_003_RECORD)
            record.record_code = '03'
            record.data_code = '62'
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.data_number = '003'
            record.address = values['street']
            return write([record])

        def set_ordering_header_004_record():
            record = Record(c34_11.ORDERING_HEADER_004_RECORD)
            record.record_code = '03'
            record.data_code = '62'
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.data_number = '004'
            record.zip = values['zip']
            record.city = values['city']
            return write([record])

        def set_national_header_record():
            record = Record(c34_11.NATIONAL_HEADER_RECORD)
            record.record_code = '04'
            record.data_code = '56'
            record.nif = values['vat_code']
            record.suffix = ''
            return write([record])

        def set_detail_001_record():
            record = Record(c34_11.DETAIL_001_RECORD)
            record.record_code = '06'
            record.data_code = values['csb34_type']
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.recipient_nif = receipt['vat_code']
            record.data_number = '010'
            record.amount = receipt['amount']
            record.account = receipt['bank_account']  # receipt['data']
            record.cost = receipt['cost']
            record.concept = receipt['concept']
            record.direct_payment = receipt['direct_payment']
            return write([record])

        def set_detail_002_record():
            record = Record(c34_11.DETAIL_002_RECORD)
            record.record_code = '06'
            record.data_code = values['csb34_type']
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.recipient_nif = receipt['vat_code']
            record.data_number = '011'
            record.name = receipt['name']
            return write([record])

        def set_detail_003_record():
            record = Record(c34_11.DETAIL_003_RECORD)
            record.record_code = '06'
            record.data_code = values['csb34_type']
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.recipient_nif = receipt['vat_code']
            record.data_number = '012'
            record.street = receipt['street']
            return write([record])

        def set_detail_004_record():
            record = Record(c34_11.DETAIL_004_RECORD)
            record.record_code = '06'
            record.data_code = values['csb34_type']
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.recipient_nif = receipt['vat_code']
            record.data_number = '013'
            record.street2 = receipt['street2']
            return write([record])

        def set_detail_005_record():
            record = Record(c34_11.DETAIL_005_RECORD)
            record.record_code = '06'
            record.data_code = values['csb34_type']
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.recipient_nif = receipt['vat_code']
            record.data_number = '014'
            record.zip = receipt['zip']
            record.city = receipt['city']
            return write([record])

        def set_detail_006_record():
            record = Record(c34_11.DETAIL_006_RECORD)
            record.record_code = '06'
            record.data_code = values['csb34_type']
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.recipient_nif = receipt['vat_code']
            record.data_number = '015'
            record.country_code = receipt['country_code']
            record.state = receipt['state']
            return write([record])

        def set_detail_007_record():
            record = Record(c34_11.DETAIL_007_RECORD)
            record.record_code = '06'
            record.data_code = values['csb34_type']
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.recipient_nif = receipt['vat_code']
            record.data_number = '016'
            record.beneficiary_nif = receipt['vat_code']
            return write([record])

        def set_national_footer_record():
            record = Record(c34_11.NATIONAL_FOOTER_RECORD)
            record.record_code = '08'
            record.data_code = '56'
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.amount = values['amount']
            record.payment_line_count = str(values['payment_count'])
            record.record_count = str(values['detail_record_count'])
            return write([record])

        def set_ordering_footer_record():
            record = Record(c34_11.ORDERING_FOOTER_RECORD)
            record.record_code = '09'
            record.data_code = '62'
            record.nif = values['vat_code']
            record.suffix = values['suffix']
            record.amount = values['amount']
            record.payment_line_count = str(values['payment_count'])
            record.record_count = str(values['record_count'])
            return write([record])

        values = Group.set_default_csb34_11_payment_values(group)
        text = set_ordering_header_record()
        values['record_count'] += 1
        text += set_ordering_header_002_record()
        values['record_count'] += 1
        text += set_ordering_header_003_record()
        values['record_count'] += 1
        text += set_ordering_header_004_record()
        values['record_count'] += 1
        text += set_national_header_record()
        values['record_count'] += 1
        values['detail_record_count'] += 1
        for receipt in values['receipts']:
            text += set_detail_001_record()
            values['record_count'] += 1
            values['detail_record_count'] += 1
            text += set_detail_002_record()
            values['record_count'] += 1
            values['detail_record_count'] += 1
            if receipt['street']:
                text += set_detail_003_record()
                values['record_count'] += 1
                values['detail_record_count'] += 1
            if 'street2' in receipt and receipt['street2']:
                text += set_detail_004_record()
                values['record_count'] += 1
                values['detail_record_count'] += 1
            if receipt['zip'] or receipt['city']:
                text += set_detail_005_record()
                values['record_count'] += 1
                values['detail_record_count'] += 1
            if values['csb34_type'] != 'transfer' and values['send_type'] in (
                    'mail', 'certified_mail'):
                text += set_detail_006_record()
                values['record_count'] += 1
                values['detail_record_count'] += 1
                if values['payroll_check']:
                    text += set_detail_007_record()
                    values['record_count'] += 1
                    values['detail_record_count'] += 1
            values['payment_count'] += 1
        values['detail_record_count'] += 1
        text += set_national_footer_record()
        values['record_count'] += 2
        text += set_ordering_footer_record()
        group.attach_file(text)
