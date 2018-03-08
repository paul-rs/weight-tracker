from abc import ABC
import json
from datetime import datetime, date
from decimal import Decimal

def json_handler(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Model):
            return value.to_json()
    raise TypeError("JSON Handler Failed on value '%s': Unknown type '%s'" % (value, type(value)))

class Model(ABC):
    def to_json_string(self):
        my_dict = {k.lstrip('_'): v for k, v in vars(self).items()}
        return json.dumps(my_dict, indent=4, default=json_handler)

    def to_json(self):
        return json.loads(self.to_json_string())


