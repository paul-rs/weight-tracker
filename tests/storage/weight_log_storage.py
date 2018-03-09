import boto3
import random
import unittest
from core.weight_log import WeightLog
from core.config import DEFAULT_REGION
from datetime import datetime
from moto.dynamodb2 import mock_dynamodb2
from storage.weight_log_storage import WeightLogStorage
from utils.random_utils import random_string, random_decimal, random_log
from dateutil.relativedelta import relativedelta


class WeightLogStorageTests(unittest.TestCase):

    def setUp(self):
        self.user_id = random_string()
        self.mock_dynamodb = mock_dynamodb2()
        self.mock_dynamodb.start()

        self.storage = WeightLogStorage(stage='dev')
        self.setup_dynamodb()
        self.addCleanup(self.mock_dynamodb.stop)

    def setup_dynamodb(self):
        dynamodb = boto3.resource('dynamodb', region_name=DEFAULT_REGION)
        dynamodb.create_table(
            TableName=self.storage.table_name,
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5,
                                   'WriteCapacityUnits': 5})

    def tearDown(self):
        try:
            client = boto3.client('dynamodb', region_name=DEFAULT_REGION)
            client.delete_table(TableName=self.storage.table_name)
            waiter = client.get_waiter('table_not_exists')
            waiter.wait(TableName=self.storage.table_name)
        except Exception:
            pass

    def test_json(self):
        log = random_log(user_id=self.user_id)
        self.assertEqual(log, WeightLog(**log.to_json()))

    def test_save_and_get(self):
        log = random_log(user_id=self.user_id)
        self.storage.save(log)
        saved_log = self.storage.get(log.user_id, log.timestamp)
        self.assertEqual(saved_log, log)

        with self.assertRaises(KeyError):
            self.storage.get(log.user_id, log.timestamp + relativedelta(years=1))

    def test_remove(self):
        log = random_log(user_id=self.user_id)
        self.storage.save(log)
        saved_log = self.storage.get(log.user_id, log.timestamp)
        self.assertEqual(saved_log, log)

        self.storage.remove(user_id=log.user_id, timestamp=log.timestamp)
        with self.assertRaises(KeyError):
            self.storage.get(log.user_id, log.timestamp)    

    def test_search_by_date(self):
        timestamp = datetime.utcnow()
        log = random_log(user_id=self.user_id)
        log.timestamp = timestamp
        self.storage.save(log)

        future = timestamp + relativedelta(years=1)
        future_log = WeightLog(
            user_id=self.user_id,
            weight=random_decimal(start=40, end=200),
            unit='kg', timestamp=future
        )
        self.storage.save(future_log)

        results = self.storage.search(
            user_id=self.user_id, start_timestamp=timestamp, end_timestamp=timestamp
        )
        self.assertEqual(len(results), 1)

        results = self.storage.search(user_id=self.user_id, start_timestamp=timestamp)
        self.assertEqual(len(results), 2)

        results = self.storage.search(user_id=self.user_id, end_timestamp=future)
        self.assertEqual(len(results), 2)

        excluded = timestamp + relativedelta(days=-1)
        results = self.storage.search(
            user_id=self.user_id, start_timestamp=excluded, end_timestamp=excluded
        )
        self.assertEqual(len(results), 0)
    
    def test_sort(self):
        count = random.randint(1, 10)
        logs = []
        for i in range(count):
            log = random_log(user_id=self.user_id)
            log.timestamp = log.timestamp + relativedelta(days=i)
            self.storage.save(log)
            logs.append(log)
        
        results = self.storage.search(user_id=self.user_id)
        results_desc = self.storage.search(user_id=self.user_id, ascending=False)

        self.assertEqual(len(results), len(results_desc))
        self.assertEqual(results, logs)
        self.assertEqual(results, list(reversed(results_desc)))

    def test_top(self):
        count = random.randint(1, 10)
        logs = []
        for i in range(count):
            log = random_log(user_id=self.user_id)
            log.timestamp = log.timestamp + relativedelta(days=i)
            self.storage.save(log)
            logs.append(log)

        results = self.storage.search(user_id=self.user_id)
        self.assertEqual(len(results), count)

        results = self.storage.search(user_id=self.user_id, top=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(logs[0], results[0])

        results = self.storage.search(user_id=self.user_id, top=1, ascending=False)
        self.assertEqual(len(results), 1)
        self.assertEqual(logs[-1], results[0])

        expected = random.randint(1, count)
        results = self.storage.search(user_id=self.user_id, top=expected)
        self.assertEqual(len(results), expected)
