from enum import Enum


class CustomerType(str, Enum):
    REGULAR = "REGULAR"
    VIP = "VIP"
    STUDENT = "STUDENT"

    