import tempfile
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from customer_types import CustomerType
from dtos import Order, OrderItem
from exceptions import InvalidQuantityError, UnknownProductError
from order_formatter import OrderFormatter
from order_io import save_order
from order_parser import parse_order
from order_processor import OrderProcessor
from pricing import calculate_total_price

ALICE = "Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10"
BOB = "Bob|bob@example.test|REGULAR|BAG:2|NONE"
ALICE_ORDER = "ORDER|Alice|BOOKx2;PENx3;|109.41"
BOB_ORDER = "ORDER|Bob|BAGx2;|196.80"
EMPTY_REPORT = "REPORT|0|0.00"
ORDERS_FILE = Path("orders.txt")


def orders_file_text() -> str:
    if not ORDERS_FILE.exists():
        return ""
    return ORDERS_FILE.read_text(encoding="utf-8")


class MainScenarioTests(unittest.TestCase):
    def test_demo_matches_main_output_without_touching_orders_file(self) -> None:
        saved: list[str] = []
        processor = OrderProcessor(order_saver=saved.append)
        stdout = StringIO()
        before = orders_file_text()

        with redirect_stdout(stdout):
            processor.process_order(ALICE, verbose=True, send=True, save=True)
            processor.process_order(BOB, verbose=True, send=True, save=True)
            processor.build_report(verbose=True)

        self.assertEqual(
            stdout.getvalue().splitlines(),
            [
                f"EMAIL alice@example.test|{ALICE_ORDER}",
                ALICE_ORDER,
                f"EMAIL bob@example.test|{BOB_ORDER}",
                BOB_ORDER,
                "REPORT|2|306.21",
            ],
        )
        self.assertEqual(saved, [ALICE_ORDER, BOB_ORDER])
        self.assertEqual(orders_file_text(), before)

    def test_disabled_side_effects_still_count_the_order(self) -> None:
        processor = OrderProcessor()
        stdout = StringIO()
        before = orders_file_text()

        with redirect_stdout(stdout):
            result = processor.process_order(
                ALICE,
                verbose=False,
                send=False,
                save=False,
            )

        self.assertEqual(result, ALICE_ORDER)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(orders_file_text(), before)
        self.assertEqual(processor.build_report(verbose=False), "REPORT|1|109.41")

    def test_notification_without_save(self) -> None:
        sent: list[str] = []
        processor = OrderProcessor(
            order_notifier=lambda email, output: sent.append(f"EMAIL {email}|{output}")
        )
        before = orders_file_text()

        result = processor.process_order(
            ALICE,
            verbose=False,
            send=True,
            save=False,
        )

        self.assertEqual(result, ALICE_ORDER)
        self.assertEqual(sent, [f"EMAIL alice@example.test|{ALICE_ORDER}"])
        self.assertEqual(orders_file_text(), before)
        self.assertEqual(processor.build_report(verbose=False), "REPORT|1|109.41")


class PricingRuleTests(unittest.TestCase):
    def test_discounts_coupon_and_delivery_threshold(self) -> None:
        cases = {
            "Ann|a@b.c|STUDENT|BAG:1|NONE": "ORDER|Ann|BAGx1;|108.24",
            "Ann|a@b.c|STUDENT|BAG:1|SAVE10": "ORDER|Ann|BAGx1;|98.89",
            "Ann|a@b.c|REGULAR|BOOK:2,PEN:4|NONE": "ORDER|Ann|BOOKx2;PENx4;|123.00",
            "Ann|a@b.c|REGULAR|BOOK:2,PEN:3|NONE": "ORDER|Ann|BOOKx2;PENx3;|131.61",
            "Ann|a@b.c|VIP|BOOK:2,PEN:3|NONE": "ORDER|Ann|BOOKx2;PENx3;|119.92",
            "alice|alice@example.test|vip|book:02,pen:3|save10": (
                "ORDER|alice|BOOKx2;PENx3;|109.41"
            ),
        }

        for raw_order, expected in cases.items():
            with self.subTest(raw_order=raw_order):
                processor = OrderProcessor()
                self.assertEqual(
                    processor.process_order(
                        raw_order,
                        verbose=False,
                        send=False,
                        save=False,
                    ),
                    expected,
                )

    def test_report_sums_unrounded_totals(self) -> None:
        raw_order = "Ann|ann@example.test|VIP|BOOK:2,PEN:3|NONE"
        processor = OrderProcessor()

        first = processor.process_order(
            raw_order,
            verbose=False,
            send=False,
            save=False,
        )
        processor.process_order(raw_order, verbose=False, send=False, save=False)

        self.assertEqual(first, "ORDER|Ann|BOOKx2;PENx3;|119.92")
        self.assertEqual(processor.build_report(verbose=False), "REPORT|2|239.85")

    def test_empty_report(self) -> None:
        self.assertEqual(
            OrderProcessor().build_report(verbose=False),
            EMPTY_REPORT,
        )

    def test_half_even_rounding(self) -> None:
        formatter = OrderFormatter()

        self.assertEqual(formatter.format_money(Decimal("1.225")), "1.22")
        self.assertEqual(formatter.format_money(Decimal("1.235")), "1.24")
        self.assertEqual(formatter.format_money(Decimal("109.4085")), "109.41")

    def test_formatter_is_shared_by_the_order_line_and_the_report(self) -> None:
        class TaggedFormatter(OrderFormatter):
            def format_money(self, amount: Decimal) -> str:
                return f"X{super().format_money(amount)}"

        processor = OrderProcessor(order_formatter=TaggedFormatter())
        result = processor.process_order(
            ALICE,
            verbose=False,
            send=False,
            save=False,
        )

        self.assertEqual(result, "ORDER|Alice|BOOKx2;PENx3;|X109.41")
        self.assertEqual(processor.build_report(verbose=False), "REPORT|1|X109.41")

    def test_unknown_product_is_rejected_by_the_calculator(self) -> None:
        order = Order(
            customer_name="Ann",
            email="ann@example.test",
            customer_type=CustomerType.REGULAR,
            items=(OrderItem(product_name="MUG", quantity=1),),
            coupon="NONE",
        )

        with self.assertRaises(UnknownProductError):
            calculate_total_price(order)


class ValidationTests(unittest.TestCase):
    def test_rejected_input_does_not_change_the_report(self) -> None:
        cases = {
            "": "ERROR|INVALID_ORDER",
            "not-an-order": "ERROR|INVALID_ORDER",
            "Ann|ann@example.test|GOLD|BOOK:1|NONE": "ERROR|INVALID_ORDER",
            "Ann|ann@example.test|REGULAR|BOOK:1|NONE|EXTRA": "ERROR|INVALID_ORDER",
            "Ann|ann@example.test|REGULAR|BOOK:x|NONE": "ERROR|INVALID_ORDER",
            "Ann|ann@example.test|REGULAR|BOOK:0|NONE": "ERROR|INVALID_QUANTITY",
            "Ann|ann@example.test|REGULAR|BOOK:-1|NONE": "ERROR|INVALID_QUANTITY",
            "Ann|ann@example.test|REGULAR|BOOK:2,PEN:0|NONE": "ERROR|INVALID_QUANTITY",
            "Ann|ann@example.test|REGULAR|MUG:0|NONE": "ERROR|INVALID_QUANTITY",
            "Ann|ann@example.test|REGULAR|MUG:1|NONE": "ERROR|UNKNOWN_PRODUCT",
            "Ann|ann@example.test|REGULAR|BOOK:1,MUG:2|NONE": "ERROR|UNKNOWN_PRODUCT",
        }

        for raw_order, expected in cases.items():
            with self.subTest(raw_order=raw_order):
                saved: list[str] = []
                sent: list[tuple[str, str]] = []
                processor = OrderProcessor(
                    order_saver=saved.append,
                    order_notifier=lambda email, output: sent.append((email, output)),
                )
                stdout = StringIO()
                with redirect_stdout(stdout):
                    result = processor.process_order(
                        raw_order,
                        verbose=True,
                        send=True,
                        save=True,
                    )

                self.assertEqual(result, expected)
                self.assertEqual(saved, [])
                self.assertEqual(sent, [])
                self.assertEqual(stdout.getvalue(), "")
                self.assertEqual(processor.build_report(verbose=False), EMPTY_REPORT)

    def test_zero_quantity_fails_in_the_parser(self) -> None:
        with self.assertRaises(InvalidQuantityError):
            parse_order("Ann|ann@example.test|REGULAR|BOOK:0|NONE")


class PersistenceTests(unittest.TestCase):
    def test_failed_save_is_not_counted_or_notified(self) -> None:
        saved: list[str] = []
        sent: list[tuple[str, str]] = []
        fail_next_save = True

        def save(output: str) -> None:
            nonlocal fail_next_save
            if fail_next_save:
                fail_next_save = False
                raise OSError("read-only")
            saved.append(output)

        processor = OrderProcessor(
            order_saver=save,
            order_notifier=lambda email, output: sent.append((email, output)),
        )
        stdout = StringIO()
        bag_one = "Bob|bob@example.test|REGULAR|BAG:1|NONE"

        with redirect_stdout(stdout):
            failed = processor.process_order(
                bag_one,
                verbose=True,
                send=True,
                save=True,
            )

        self.assertEqual(failed, "ERROR|SAVE_FAILED")
        self.assertEqual(saved, [])
        self.assertEqual(sent, [])
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(processor.build_report(verbose=False), EMPTY_REPORT)

        processed = processor.process_order(
            BOB,
            verbose=False,
            send=True,
            save=True,
        )

        self.assertEqual(processed, BOB_ORDER)
        self.assertEqual(saved, [BOB_ORDER])
        self.assertEqual(sent, [("bob@example.test", BOB_ORDER)])
        self.assertEqual(processor.build_report(verbose=False), "REPORT|1|196.80")

    def test_unexpected_save_error_propagates_without_counting(self) -> None:
        def save(_output: str) -> None:
            raise ValueError("boom")

        processor = OrderProcessor(order_saver=save)

        with self.assertRaises(ValueError):
            processor.process_order(ALICE, verbose=False, send=False, save=True)

        self.assertEqual(processor.build_report(verbose=False), EMPTY_REPORT)

    def test_save_order_appends_lines(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "orders.txt"
            with patch("order_io.ORDERS_FILE", path):
                save_order(ALICE_ORDER)
                save_order(BOB_ORDER)

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                f"{ALICE_ORDER}\n{BOB_ORDER}\n",
            )


class ApiTests(unittest.TestCase):
    def test_flags_are_keyword_only(self) -> None:
        processor = OrderProcessor()

        with self.assertRaises(TypeError):
            processor.process_order(ALICE, False, False, False)
        with self.assertRaises(TypeError):
            processor.build_report(False)


if __name__ == "__main__":
    unittest.main()
