from dataclasses import dataclass

from customer_types import CustomerType


@dataclass(frozen=True, slots=True)
class OrderItem:
    product_name: str
    quantity: int


@dataclass(frozen=True, slots=True)
class Order:
    customer_name: str
    email: str
    customer_type: CustomerType
    items: list[OrderItem]
    coupon: str
