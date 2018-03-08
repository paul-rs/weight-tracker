import boto3
from core.config import DEFAULT_REGION
from datetime import datetime


class DynamoDBStorage():

    def __init__(self, table_name, region=DEFAULT_REGION):
        self.table_name = table_name
        self.__dynamodb = boto3.resource('dynamodb', region_name=region)
        self.__table = self.__dynamodb.Table(self.table_name)
    
    def save(self, weight_record):
        self.__table.put_item(Item=weight_record.to_json())
    
    def remove(self, weight_record):
        pass
    
    def get(self, user_id, **params):
        pass