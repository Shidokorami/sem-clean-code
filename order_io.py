from pathlib import Path


ORDERS_FILE = Path("orders.txt")


def save_order(output: str) -> None:
    with ORDERS_FILE.open("a", encoding="utf-8") as file:
        file.write(f"{output}\n")


def send_order_notification(email: str, output: str) -> None:
    print(f"EMAIL {email}|{output}")
