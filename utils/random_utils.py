import random
import string
from decimal import Decimal

def random_string(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_decimal(start=0, end=1000):
    return Decimal(random.randrange(start * 100, end * 100))/100