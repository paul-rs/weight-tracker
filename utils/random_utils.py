import random
import string
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from datetime import datetime
from core.user import User
from core.weight_log import WeightLog

def random_string(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_decimal(start=0, end=1000):
    return Decimal(random.randrange(start * 100, end * 100))/100

def random_user():
    current_weight = random_decimal(start=40, end=200)
    return User(
        user_id=random_string(), weight=current_weight,
        target_weight=current_weight - random_decimal(5, 20),
        target_date=datetime.utcnow() + relativedelta(weeks=6),
        name=random_string(), age=random_decimal(18, 100),
        gender=random.choice(['M', 'F']), height=random_decimal(100, 250),
        unit_preference='kg'
    )

def random_log(user_id=None):
    user_id = user_id or random_string()
    return WeightLog(
        user_id=user_id,
        weight=random_decimal(start=40, end=200),
        unit='kg', timestamp=datetime.utcnow()
    )