from core.user import User
from core.weight_log import WeightLog
from storage.user_storage import UserStorage
from storage.weight_log_storage import WeightLogStorage


class WeightTracker():

    def __init__(self, stage):
        self.stage = stage