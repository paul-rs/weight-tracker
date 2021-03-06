from core.model import Model
from decimal import Decimal, InvalidOperation
from dateutil.parser import parse
from datetime import date, datetime


class User(Model):

    def __init__(self, user_id, weight, 
                 target_weight, target_date,
                 name=None, age=None, gender=None,
                 height=None, unit_preference=None):
        self.user_id = user_id
        self.weight = weight
        self.target_weight = target_weight
        self.target_date = target_date
        self.name = name
        self.age = age
        self.height = height
        self.gender = gender
        self.unit_preference = unit_preference or 'kg'
    
    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, value):
        # todo: wrap/reuse this kind of validation
        try:
            value = Decimal(value)
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError(f'Could not convert {value} to a decimal value.')
        
        if value < 1:
            raise ValueError(f'Must be a positive value.')
        else:
            self._weight = value
    
    @property
    def target_weight(self):
        return self._target_weight
    
    @target_weight.setter
    def target_weight(self, value):
        try:
            value = Decimal(value)
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError(f'Could not convert {value} to a decimal value.')
        
        if value < 1:
            raise ValueError(f'Must be a positive value.')
        else:
            self._target_weight = value
    
    @property
    def target_date(self):
        return self._target_date

    @target_date.setter
    def target_date(self, value):
        if not value:
            raise ValueError('Missing required attribute "target_date".')
        
        if isinstance(value, str):
            self._target_date = parse(value).date()
        elif isinstance(value, datetime):
            self._target_date = value.date()
        elif isinstance(value, date):
            self._target_date = value
        else:
            raise TypeError('Invalid type for attribute "target_date".')