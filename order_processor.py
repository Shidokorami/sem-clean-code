from decimal import Decimal

from order_formatter import format_money, format_order
from order_io import save_order, send_order_notification
from order_parser import parse_order
from pricing import calculate_total_price


class OrderProcessor:
    def __init__(
        self,
        price_calculator=calculate_total_price,
        order_formatter=format_order,
        order_saver=save_order,
        order_notifier=send_order_notification,
    ) -> None:
        self._processed_order_count = 0
        self._orders_total = Decimal("0.00")
        self._price_calculator = price_calculator
        self._order_formatter = order_formatter
        self._order_saver = order_saver
        self._order_notifier = order_notifier

    def process_order(
        self,
        raw_order: str,
        verbose: bool,
        send: bool,
        save: bool,
    ) -> str:
        try:
            order = parse_order(raw_order)
            total_price = self._price_calculator(order)
            output = self._order_formatter(order, total_price)

            self._processed_order_count += 1
            self._orders_total += total_price

            if save:
                self._order_saver(output)

            if send:
                self._order_notifier(order.email, output)

            if verbose:
                print(output)

            return output
        except Exception:
            return "ERROR"

    def build_report(self, verbose: bool) -> str:
        report = (
            f"REPORT|{self._processed_order_count}|"
            f"{format_money(self._orders_total)}"
        )

        if verbose:
            print(report)

        return report
