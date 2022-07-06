from enum import Enum
from typing import List


class Subscription(str, Enum):
    free = 'free'
    normal = 'normal'
    premium = 'premium'

    def get_allowed(subscription: str) -> List[str]:
        if subscription == "premium":
            return ["free", "premium", "normal"]
        if subscription == "normal":
            return ["free", "normal"]
        if subscription == "free":
            return ["free"]
        return [""]
