from customer_types import CustomerType
from dtos import Order, OrderItem


class OrderParseError(ValueError):
    """Dane wejściowe nie mają poprawnego formatu zamówienia."""


def parse_customer_type(raw_customer_type: str) -> CustomerType:
    return CustomerType(raw_customer_type.strip().upper())


def parse_items(raw_items: str) -> tuple[OrderItem, ...]:
    items: list[OrderItem] = []

    for raw_item in raw_items.split(","):
        product_name, raw_quantity = raw_item.split(":")
        items.append(
            OrderItem(
                product_name=product_name.strip().upper(),
                quantity=int(raw_quantity),
            )
        )

    return tuple(items)


def parse_order(raw_order: str) -> Order:
    try:
        customer_name, email, raw_customer_type, raw_items, coupon = raw_order.split(
            "|"
        )

        return Order(
            customer_name=customer_name,
            email=email,
            customer_type=parse_customer_type(raw_customer_type),
            items=parse_items(raw_items),
            coupon=coupon.strip().upper(),
        )
    except ValueError as error:
        raise OrderParseError("Niepoprawny format zamówienia.") from error
