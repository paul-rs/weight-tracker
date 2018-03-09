import boto3
from boto3.dynamodb.conditions import Key, Attr
from core.config import DEFAULT_REGION
from core.user import User
from datetime import datetime

class UserStorage():

    def __init__(self, stage, region=DEFAULT_REGION):
        self.stage = stage
        self.table_name = '-'.join(['users', stage])
        self.__dynamodb = boto3.resource('dynamodb', region_name=region)
        self.__table = self.__dynamodb.Table(self.table_name)
    
    def save(self, user):
        self.__table.put_item(Item=user.to_json())
    
    def remove(self, user_id):
        self.__table.delete_item(Key=dict(user_id=user_id))

    def get(self, user_id):
        response = self.__table.get_item(Key=dict(user_id=user_id))
        item = response.get('Item')

        if item:
            return User(**item)
        
        raise KeyError(f'Could not find user with id {user_id}.')
