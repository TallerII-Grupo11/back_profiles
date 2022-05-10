from enum import Enum
from typing import List


class Subscription(str, Enum):
    free = 'free'
    premium = 'premium'
    plus = 'plus'

    def get_allowed(subscription: str) -> List[str]:
        if (subscription == "plus"):
            return ["free", "premium", "plus"]
        if (subscription == "premium"):
            return ["free", "premium"]
        return ["free"]
