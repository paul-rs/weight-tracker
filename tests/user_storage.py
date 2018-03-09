import boto3
import random
import unittest
from core.user import User
from core.config import DEFAULT_REGION
from datetime import datetime
from moto.dynamodb2 import mock_dynamodb2
from storage.user_storage import UserStorage
from utils.random_utils import random_string, random_decimal
from dateutil.relativedelta import relativedelta


class UserStorageTests(unittest.TestCase):

    def setUp(self):
        self.storage = UserStorage(stage='dev')

        self.mock_dynamodb = mock_dynamodb2()
        self.mock_dynamodb.start()

        self.setup_dynamodb()
    
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
        finally:
            self.mock_dynamodb.stop()
    
    def random_user(self):
        current_weight = random_decimal(start=40, end=200)
        return User(
            user_id=random_string(), weight=current_weight,
            target_weight=current_weight - random_decimal(5, 20),
            target_date=datetime.utcnow() + relativedelta(weeks=6),
            name=random_string(), age=random_decimal(18, 100),
            gender=random.choice(['M', 'F']), height=random_decimal(100, 250),
            unit_preference='kg'
        )

    def test_json(self):
        user = self.random_user()
        self.assertEqual(user, User(**user.to_json()))

    def test_save(self):
        user = self.random_user()
        self.storage.save(user)
        saved_user = self.storage.get(user_id=user.user_id)
        self.assertEqual(saved_user, user)


