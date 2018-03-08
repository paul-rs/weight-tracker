from dateutil.parser import parse
from datetime import datetime, date
from core.model import Model
from decimal import Decimal

class WeightRecord(Model):

    def __init__(self, user_id, weight, unit, timestamp):
        self.user_id = user_id
        self.weight = weight
        self.unit = unit
        self.timestamp = timestamp
    
    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, value):
        try:
            self._weight = Decimal(value)
        except ValueError:
            raise ValueError(f'Could not convert {value} to an decimal value.')

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if not value:
            raise ValueError('Missing required attribute "timestamp".')
        
        if isinstance(value, str):
            self._timestamp = parse(value)
        elif isinstance(value, datetime):
            self._timestamp = value
        else:
            raise TypeError('Invalid type for attribute "timestamp".')