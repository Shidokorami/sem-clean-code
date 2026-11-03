from decimal import Decimal

from dtos import Order


def format_money(amount: Decimal) -> str:
    return f"{amount:.2f}"


def format_order_items(order: Order) -> str:
    return "".join(
        f"{item.product_name}x{item.quantity};"
        for item in order.items
    )


def format_order(order: Order, total_price: Decimal) -> str:
    item_details = format_order_items(order)
    return f"ORDER|{order.customer_name}|{item_details}|{format_money(total_price)}"
