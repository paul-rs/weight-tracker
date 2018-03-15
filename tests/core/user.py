import unittest
from copy import deepcopy
from datetime import datetime, date
from dateutil.parser import parse
from decimal import Decimal
from utils.random_utils import random_user, random_string, random_decimal
from core.user import User


class UserTests(unittest.TestCase):

    def test_eq(self):
        user = random_user()
        user_2 = deepcopy(user)
        self.assertEqual(user, user_2)
        self.assertEqual(hash(user), hash(user_2))

    def test_json(self):
        user = random_user()
        user_2 = User(**user.to_json())
        self.assertEqual(user, user_2)
        self.assertEqual(hash(user), hash(user_2))
    
    def test_weight_properties(self):
        valid_values = [100, '100', '100.23', Decimal(100)]
        invalid_values = [None, '', 'One hundred', 0, -100, False]

        for value in valid_values:
            for w, tw, prop in [(value, random_decimal(), 'weight'),
                               (random_decimal(), value, 'target_weight')]:
                user = User(
                    user_id=random_string(),
                    weight=w,
                    target_weight=tw,
                    target_date=datetime.utcnow()
                )
                self.assertEqual(getattr(user, prop), Decimal(value))
        
        for value in invalid_values:
            for w, tw in [(value, random_decimal()),
                          (random_decimal(), value)]:
                with self.assertRaises(ValueError):
                    user = User(
                        user_id=random_string(),
                        weight=w,
                        target_weight=tw, 
                        target_date=datetime.utcnow()
                    )
    
    def test_target_date(self):
        valid_values = [datetime(2018,1,1,12,30), date(2018,1,1), '2018-01-01', '2018-03-09T06:29:16.660417']
        invalid_values = [None, 0, 100, 'today']

        for value in valid_values:
            user = User(
                user_id=random_string(),
                weight=random_decimal(),
                target_weight=random_decimal(),
                target_date=value
            )
            if isinstance(value, (date, datetime)):
                expected = parse(value.isoformat()).date()
            else:
                expected = parse(value).date()

            self.assertEqual(user.target_date, expected)
        
        for value in invalid_values:
            with self.assertRaises(Exception):
                user = User(
                    user_id=random_string(),
                    weight=random_decimal(),
                    target_weight=random_decimal(),
                    target_date=value
                )