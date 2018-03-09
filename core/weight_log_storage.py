import boto3
from boto3.dynamodb.conditions import Key, Attr
from core.config import DEFAULT_REGION
from core.weight_log import WeightLog
from datetime import datetime

class WeightLogStorage():

    def __init__(self, stage, region=DEFAULT_REGION):
        self.stage = stage
        self.table_name = '-'.join(['weight-logs', stage])
        self.__dynamodb = boto3.resource('dynamodb', region_name=region)
        self.__table = self.__dynamodb.Table(self.table_name)

    def save(self, weight_record):
        self.__table.put_item(Item=weight_record.to_json())

    def remove(self, weight_record):
        pass

    def get(self, user_id, timestamp):
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()

        params = dict(Key={'user_id': user_id, 'timestamp': timestamp})
        results = self.__table.get_item(**params)
        item = results.get('Item')

        if item:
            return WeightLog(**item)
        else:
            raise KeyError(f'Could not find weight record for user {user_id} with timestamp {timestamp}.')

    def search(self, user_id, **kwargs):
        """
        Searches the weight logs table for matching entries.

        Args:
            user_id (str): The user id hash key.
            top (int): The number of results to return sorted by timestamp.
            ascending (bool): Sort order of the records using timestamp sort key. Defaults to True.
            start_timestamp (datetime): Forms the start of the date range filter compared to timestamp.
            end_timestamp (datetime): Forms the end of the date range filter compared to timestamp.
        """
        params = dict(TableName=self.table_name)
        key_cond = Key('user_id').eq(user_id)
        
        start_date = kwargs.pop('start_timestamp', None)
        end_date = kwargs.pop('end_timestamp', None)
        if start_date or end_date:
            start_date = start_date or datetime.min
            end_date = end_date or datetime.max
            date_cond = Key('timestamp').between(start_date.isoformat(), end_date.isoformat())
            key_cond = key_cond & date_cond
        
        params.update(dict(KeyConditionExpression=key_cond))
        result_count = kwargs.pop('top', None) 
        asc = kwargs.pop('ascending', True)
        params.update(dict(ScanIndexForward=asc))

        results = []
        last_eval = None
        while True:
            response = self.__table.query(**params)
            results += response.get('Items', [])

            if result_count and len(results) >= result_count:
                results = results[:result_count]
                break

            last_eval = response.get('LastEvaluatedKey')
            if not last_eval:
                break
            else:
                params.update(dict(ExclusiveStartKey=last_eval))

        return [WeightLog(**r) for r in results]


