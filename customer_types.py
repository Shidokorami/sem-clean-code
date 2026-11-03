from enum import Enum
from decimal import Decimal


class CustomerType(str, Enum):
    REGULAR = "REGULAR"
    VIP = "VIP"
    STUDENT = "STUDENT"



REGULAR = "REGULAR"
VIP = "VIP"
STUDENT = "STUDENT"


CUSTOMER_DISCOUNTS: dict[str, Decimal] = {
    REGULAR: Decimal("0.00"),
    VIP: Decimal("0.10"),
    STUDENT: Decimal("0.05"),
}
    