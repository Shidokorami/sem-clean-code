from decimal import Decimal

BOOK = "BOOK"
PEN = "PEN"
BAG = "BAG"

PRODUCT_PRICES: dict[str, Decimal] = {
    BOOK: Decimal("40.00"),
    PEN: Decimal("5.00"),
    BAG: Decimal("80.00"),
}
