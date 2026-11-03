# Order Processor Refactoring

## Goal

The original implementation combined input parsing, price calculations, reporting, file storage and notifications in a single function named `doIt`.

The refactoring separates these responsibilities, improves naming and removes unnecessary code. This document describes the changes compared with that original implementation.

## 1. Meaningful names

Names such as `doIt`, `a`, `b`, `c`, `z` and `x` were replaced with names describing their purpose, such as `process_order`, `order`, `items_subtotal`, `total_price` and `output`.

**Principle: intention-revealing names.**

The code is easier to understand without tracing every variable or adding comments that explain basic operations.

## 2. Separate order processing and reporting

The original function used numeric action codes to choose an operation:

- `1` processed an order.
- `2` generated a report.

These were replaced with separate methods: `process_order` and `build_report`.

**Principles: clear interfaces and KISS.**

Callers can select an operation by its name instead of remembering numeric codes. Each method has a clearer purpose.

## 3. Separation of responsibilities

The original `doIt` function performed several unrelated tasks. These responsibilities were moved into dedicated modules:

| Module | Responsibility |
| --- | --- |
| `main.py` | Runs the demonstration scenario. |
| `dtos.py` | Defines order data structures. |
| `customer_types.py` | Defines supported customer types. |
| `product_prices.py` | Defines product prices. |
| `order_parser.py` | Parses input text. |
| `pricing.py` | Calculates prices, discounts, delivery and tax. |
| `order_formatter.py` | Formats order results and monetary values. |
| `order_io.py` | Saves orders and simulates notifications. |
| `order_processor.py` | Coordinates processing and maintains report state. |

**Principle: Single Responsibility Principle (SRP).**

Changes to parsing, pricing or storage can be made in their respective modules. For example, changing product prices does not require editing file-writing code.

## 4. Explicit and immutable order data

The original code accessed order information through positional indexes such as `a[0]` and `a[4]`.

The refactored code introduces the dataclasses `Order` and `OrderItem`. Their named fields describe the information being processed.

The dataclasses use `frozen=True`, and order items are stored in a tuple. This prevents ordinary field reassignment and modification of the item collection.

**Principles: meaningful data structures and limited mutation.**

The rest of the program works with named fields instead of depending on the input text layout. Order data cannot be accidentally modified in place during processing.

## 5. Small calculation functions

The calculations previously embedded in `doIt` were extracted into focused functions:

- `calculate_items_subtotal`
- `apply_customer_discount`
- `apply_coupon_discount`
- `add_delivery_fee_if_needed`
- `apply_tax`

The `calculate_total_price` function coordinates these steps.

**Principle: small functions with one clear purpose.**

Each calculation can be understood independently. The coordinating function presents the business rules in their execution order.

## 6. Named constants and business rule tables

Hard-coded values were replaced with constants such as `DELIVERY_FEE`, `FREE_DELIVERY_THRESHOLD` and `TAX_RATE`.

Product prices and customer discounts are stored in dictionaries instead of conditional chains. Customer types are represented by the `CustomerType` enum.

The enum is defined in `customer_types.py`, while customer discount values are defined in `pricing.py`.

**Principles: descriptive constants, DRY and support for the Open/Closed Principle.**

Business values have clear names and a single definition. Adding a product price does not require extending the calculation algorithm with another conditional branch.

## 7. Removal of unnecessary inheritance

The original `Everything` class grouped saving, sending and refunding. Its subclass, `Thing`, rejected the refund operation.

These classes were replaced with separate functions for saving and notification. The unsupported refund operation was removed.

**Principles: Interface Segregation Principle (ISP), KISS and YAGNI.**

The processor depends only on the capabilities it uses. There is no need to maintain an inheritance hierarchy or an operation without a current requirement.

## 8. Dependency injection

The original function constructed `Thing` directly, tying processing to its file and console operations.

The refactored `OrderProcessor` receives the calculator, formatter, saver and notifier through its constructor.

**Connection to the Dependency Inversion Principle (DIP).**

The workflow can use different implementations supplied by the caller. Replacing storage or notification behavior does not require changing the processing method.

## 9. Encapsulated state and removal of unused code

The global `counter` and `total` variables were replaced with instance attributes in `OrderProcessor`.

The following unused elements were removed:

- `mode`
- `future_currencies`
- The `unused` parameter.
- The cache, which was written to but never read.

**Principles: encapsulation, avoidance of shared mutable state and YAGNI.**

Each processor owns its report state. Removing unused elements reduces the amount of code and state that must be understood and maintained.

## 10. Decimal arithmetic

The original program used binary floating-point arithmetic for discounted and taxed amounts.

The refactored implementation uses `Decimal`, with constants constructed from strings. Output is still formatted to two decimal places, and reports sum amounts before display formatting.

**Principle: use data types appropriate to the domain.**

Decimal arithmetic avoids binary representation errors for the decimal values used in the pricing rules. However, results can differ from the original floating-point implementation in rounding-sensitive cases.

## 11. Specific error handling

The original `except Exception` converted every failure into `"ERROR"`.

The refactored parser raises `OrderParseError` for invalid input. The processor handles parsing errors separately from storage errors:

| Failure | Result |
| --- | --- |
| Invalid input | `ERROR|INVALID_ORDER` |
| Storage failure reported as `OSError` | `ERROR|SAVE_FAILED` |

Unexpected exceptions are allowed to propagate instead of being hidden.

**Principle: handle specific errors at the appropriate boundary.**

Expected failures can be distinguished, while programming defects remain visible for diagnosis.

## Business rules retained

The pricing sequence remains:

1. Calculate the product subtotal.
2. Apply the customer discount.
3. Apply the coupon discount.
4. Add delivery if the discounted subtotal is below 100.00.
5. Apply 23% tax, including delivery.
6. Format the amount to two decimal places.

Successful order and report output retain the `ORDER|...` and `REPORT|...` structures. Notifications retain the `EMAIL` prefix.

## Behavior changes

Some changes go beyond structural refactoring:

- Unknown customer types now produce `ERROR|INVALID_ORDER` instead of receiving no customer discount.
- Product names, customer types and coupons are normalized by trimming surrounding whitespace and converting letters to uppercase.
- Quantities are formatted as integers, so `BOOK:02` produces `BOOKx2;` instead of `BOOKx02;`.
- The parser requires exactly five fields, while the original ignored additional fields.
- Parsing and storage failures return different error messages.
- Unexpected exceptions can propagate.
- Separate methods replace the original action-based API.
- Decimal arithmetic may change rounding results.
