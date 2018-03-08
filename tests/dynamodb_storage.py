import unittest
from core.dynamodb_storage import DynamoDBStorage
from core.weight_record import WeightRecord
from utils.random_utils import random_string, random_decimal
from datetime import datetime

# todo: mock dynamodb
class DynamoDBStorageTests(unittest.TestCase):

    def setUp(self):
        self.storage = DynamoDBStorage(table_name='weights-dev')
    
    def test_save(self):
        record = WeightRecord(
            user_id=random_string(),
            weight=random_decimal(start=40, end=200),
            unit='kg', timestamp=datetime.utcnow()
        )
        self.storage.save(record)
        # fetch, then assert