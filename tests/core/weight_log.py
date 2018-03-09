import unittest
from decimal import Decimal
from datetime import datetime, date
from dateutil.parser import parse
from utils.random_utils import random_log, random_string, random_decimal
from core.weight_log import WeightLog


class WeightLogTests(unittest.TestCase):
   
    def test_equality(self):
        log = random_log()
        log_2 = WeightLog(**log.to_json())
        self.assertEqual(log, log_2)
        self.assertEqual(hash(log), hash(log_2))
        self.assertNotEqual(log, None)
    
    def test_weight_property(self):
        valid_values = [100, '100', '100.23', Decimal(100)]
        invalid_values = [None, '', 'One hundred', 0, -100, False]

        for value in valid_values:
            log = WeightLog(
                user_id=random_string(), weight=value, unit='kg', timestamp=datetime.utcnow()
            )
            self.assertEqual(log.weight, Decimal(value))
        
        for value in invalid_values:
            with self.assertRaises(ValueError):
                log = WeightLog(
                    user_id=random_string(), weight=value, unit='kg', timestamp=datetime.utcnow()
                )
    
    def test_timestamp(self):
        valid_values = [datetime(2018,1,1,12,30), date(2018,1,1), '2018-01-01', '2018-03-09T06:29:16.660417']
        invalid_values = [None, 0, 100, 'today']

        for value in valid_values:
            log = WeightLog(
                user_id=random_string(), weight=random_decimal(), unit='kg', timestamp=value
            )
            if isinstance(value, (date, datetime)):
                expected = parse(value.isoformat())
            else:
                expected = parse(value)

            self.assertEqual(log.timestamp, expected)
        
        for value in invalid_values:
            with self.assertRaises(Exception):
                log = WeightLog(
                    user_id=random_string(), weight=random_decimal(), unit='kg', timestamp=value
                )