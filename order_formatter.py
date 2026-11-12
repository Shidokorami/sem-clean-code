from decimal import ROUND_HALF_EVEN, Decimal

from dtos import Order

CENT = Decimal("0.01")


class OrderFormatter:
    def format_money(self, amount: Decimal) -> str:
        rounded = amount.quantize(CENT, rounding=ROUND_HALF_EVEN)
        return f"{rounded:.2f}"

    def format_order(self, order: Order, total_price: Decimal) -> str:
        item_details = self._format_items(order)
        return f"ORDER|{order.customer_name}|{item_details}|{self.format_money(total_price)}"

    def _format_items(self, order: Order) -> str:
        return "".join(f"{item.product_name}x{item.quantity};" for item in order.items)
