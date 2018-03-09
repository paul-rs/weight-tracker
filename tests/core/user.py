import unittest
from utils.random_utils import random_user
from core.user import User


class UserTests(unittest.TestCase):

     def test_json(self):
        user = random_user()
        user_2 = User(**user.to_json())
        self.assertEqual(user, user_2)
        self.assertEqual(hash(user), hash(user_2))
