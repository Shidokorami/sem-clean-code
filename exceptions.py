class OrderError(Exception):
    code: str


class OrderParseError(OrderError):
    code = "INVALID_ORDER"


class InvalidQuantityError(OrderError):
    code = "INVALID_QUANTITY"


class UnknownProductError(OrderError):
    code = "UNKNOWN_PRODUCT"
