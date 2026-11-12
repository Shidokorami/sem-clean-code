from collections.abc import Callable
from decimal import Decimal
from typing import Optional

from dtos import Order
from exceptions import OrderError
from order_formatter import OrderFormatter
from order_io import save_order, send_order_notification
from order_parser import parse_order
from pricing import calculate_total_price

PriceCalculator = Callable[[Order], Decimal]
OrderSaver = Callable[[str], None]
OrderNotifier = Callable[[str, str], None]


class OrderProcessor:
    def __init__(
        self,
        price_calculator: PriceCalculator = calculate_total_price,
        order_formatter: Optional[OrderFormatter] = None,
        order_saver: OrderSaver = save_order,
        order_notifier: OrderNotifier = send_order_notification,
    ) -> None:
        self._processed_order_count = 0
        self._orders_total = Decimal("0.00")
        self._price_calculator = price_calculator
        self._order_formatter = (
            OrderFormatter() if order_formatter is None else order_formatter
        )
        self._order_saver = order_saver
        self._order_notifier = order_notifier

    def process_order(
        self,
        raw_order: str,
        *,
        verbose: bool,
        send: bool,
        save: bool,
    ) -> str:
        try:
            order = parse_order(raw_order)
            total_price = self._price_calculator(order)
        except OrderError as error:
            return f"ERROR|{error.code}"

        output = self._order_formatter.format_order(order, total_price)

        if save:
            try:
                self._order_saver(output)
            except OSError:
                return "ERROR|SAVE_FAILED"

        if send:
            self._order_notifier(order.email, output)

        self._processed_order_count += 1
        self._orders_total += total_price

        if verbose:
            print(output)

        return output

    def build_report(self, *, verbose: bool) -> str:
        report = (
            f"REPORT|{self._processed_order_count}|"
            f"{self._order_formatter.format_money(self._orders_total)}"
        )

        if verbose:
            print(report)

        return report
