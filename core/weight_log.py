from dateutil.parser import parse
from datetime import datetime, date
from core.model import Model
from decimal import Decimal, InvalidOperation

class WeightLog(Model):

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
            value = Decimal(value)
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError(f'Could not convert {value} to a decimal value.')
        
        if value < 1:
            raise ValueError(f'Must be a positive value.')
        else:
            self._weight = value

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
        elif isinstance(value, date):
            self._timestamp = datetime.combine(value, datetime.min.time())
        else:
            raise TypeError('Invalid type for attribute "timestamp".')
    
    def __repr__(self):
        return ':'.join([self.user_id, self.timestamp.isoformat()])