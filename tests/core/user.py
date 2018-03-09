import unittest
from utils.random_utils import random_user
from core.user import User


class UserTests(unittest.TestCase):

     def test_json(self):
        user = random_user()
        self.assertEqual(user, User(**user.to_json()))
