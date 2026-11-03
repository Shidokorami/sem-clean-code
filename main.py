from order_processor import OrderProcessor


if __name__ == "__main__":
    processor = OrderProcessor()

    processor.process_order(
        "Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10",
        verbose=True,
        send=True,
        save=True,
    )
    processor.process_order(
        "Bob|bob@example.test|REGULAR|BAG:2|NONE",
        verbose=True,
        send=True,
        save=True,
    )
    processor.build_report(verbose=True)
