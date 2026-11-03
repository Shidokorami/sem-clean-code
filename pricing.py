from decimal import Decimal

from customer_types import CustomerType
from dtos import Order, OrderItem
from product_prices import PRODUCT_PRICES

SAVE10 = "SAVE10"

ONE = Decimal("1.00")
DELIVERY_FEE = Decimal("12.00")
FREE_DELIVERY_THRESHOLD = Decimal("100.00")
TAX_RATE = Decimal("0.23")

CUSTOMER_DISCOUNTS: dict[CustomerType, Decimal] = {
    CustomerType.REGULAR: Decimal("0.00"),
    CustomerType.VIP: Decimal("0.10"),
    CustomerType.STUDENT: Decimal("0.05"),
}

COUPON_DISCOUNTS: dict[str, Decimal] = {
    SAVE10: Decimal("0.10"),
}


def calculate_items_subtotal(items: tuple[OrderItem, ...]) -> Decimal:
    total = Decimal("0.00")

    for item in items:
        price = PRODUCT_PRICES.get(item.product_name, Decimal("0.00"))
        total += price * item.quantity

    return total


def apply_customer_discount(amount: Decimal, customer_type: CustomerType) -> Decimal:
    discount = CUSTOMER_DISCOUNTS[customer_type]
    return amount * (ONE - discount)


def apply_coupon_discount(amount: Decimal, coupon: str) -> Decimal:
    discount = COUPON_DISCOUNTS.get(coupon, Decimal("0.00"))
    return amount * (ONE - discount)


def add_delivery_fee_if_needed(amount: Decimal) -> Decimal:
    if amount < FREE_DELIVERY_THRESHOLD:
        return amount + DELIVERY_FEE

    return amount


def apply_tax(amount: Decimal) -> Decimal:
    return amount * (ONE + TAX_RATE)


def calculate_total_price(order: Order) -> Decimal:
    items_subtotal = calculate_items_subtotal(order.items)
    after_customer_discount = apply_customer_discount(
        items_subtotal,
        order.customer_type,
    )
    after_coupon_discount = apply_coupon_discount(
        after_customer_discount,
        order.coupon,
    )
    with_delivery = add_delivery_fee_if_needed(after_coupon_discount)
    total_with_tax = apply_tax(with_delivery)

    return total_with_tax
