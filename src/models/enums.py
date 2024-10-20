import enum

class FriendsTask(enum.Enum):
    JOIN_CHANNEL = "join_channel"
    ACTIVE_TICKETS = "active_tickets"
    REFER_A_FRIEND = "refer_a_friend"
    SECRET_CODE = "secret_code"
    WATCH_ADS = "watch_ads"


class TaskStatus(enum.Enum):
    NOT_DONE = "not_done"
    DONE = "done"
    CLAIMED = "claimed"


    def is_todo(self) -> bool:
        return self == TaskStatus.NOT_DONE

class LogTag(enum.Enum):
    PUSH = "push"
    SECRET = "secret"
    SCRATCH = "scratch"
    ADS_DOUBLE = "ads_double"
    ADS_POINT = "ads_point"

