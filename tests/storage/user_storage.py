import boto3
import random
import unittest
from core.user import User
from core.config import DEFAULT_REGION
from datetime import datetime
from moto.dynamodb2 import mock_dynamodb2
from storage.user_storage import UserStorage
from utils.random_utils import random_string, random_decimal, random_user
from dateutil.relativedelta import relativedelta


class UserStorageTests(unittest.TestCase):

    def setUp(self):
        self.mock_dynamodb = mock_dynamodb2()
        self.mock_dynamodb.start()
        
        self.storage = UserStorage(stage='dev')
        self.setup_dynamodb()
        self.addCleanup(self.mock_dynamodb.stop)
    
    def setup_dynamodb(self):
        dynamodb = boto3.resource('dynamodb', region_name=DEFAULT_REGION)
        dynamodb.create_table(
            TableName=self.storage.table_name,
            KeySchema=[{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'user_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5})
    
    def tearDown(self):
        try:
            client = boto3.client('dynamodb', region_name=DEFAULT_REGION)
            client.delete_table(TableName=self.storage.table_name)
            waiter = client.get_waiter('table_not_exists')
            waiter.wait(TableName=self.storage.table_name)
        except Exception:
            pass

    def test_save_and_get(self):
        user = random_user()
        self.storage.save(user)
        saved_user = self.storage.get(user_id=user.user_id)
        self.assertEqual(saved_user, user)

        with self.assertRaises(KeyError):
            self.storage.get(user_id=user.user_id * 2)
    
    def test_remove(self):
        user = random_user()
        self.storage.save(user)
        saved_user = self.storage.get(user.user_id)
        self.assertEqual(saved_user, user)

        self.storage.remove(user_id=user.user_id)
        with self.assertRaises(KeyError):
            self.storage.get(user.user_id)    



