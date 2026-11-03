# The Order Processor Nobody Wants to Maintain

This small program is intentionally difficult to maintain. It is a teaching exercise, not an example of recommended design. Choose ONE implementation: Java, Python, or JavaScript. Each implements the same demonstration scenario without external dependencies.

## Run

Run commands from the directory containing the source files:

- Java 17 or later: `java Main.java`
- Python 3.9 or later: `python3 main.py`
- Node.js 18 or later: `node main.js`

Each run appends two lines to `orders.txt` in the current directory. Console messages beginning with EMAIL simulate notifications; no messages are actually sent. Running another implementation appends to the same file, so remove it between runs when comparing file contents. In-memory counters start at zero for each process.

## Business scenario

An order is represented by:

`customerName|email|customerType|product:quantity,product:quantity|coupon`

Products: BOOK costs 40.00, PEN costs 5.00, BAG costs 80.00. All amounts use the same unspecified currency.

Apply rules in this exact order:

1. Calculate the item subtotal.
2. Apply a customer discount: VIP 10%, STUDENT 5%, REGULAR 0%.
3. Apply an additional 10% discount for coupon SAVE10.
4. Add 12.00 delivery if the discounted subtotal is strictly below 100.00.
5. Apply 23% tax to the resulting amount, including delivery.
6. Display money with two decimal places.

The report contains the processed order count and sum of unrounded order totals, formatted to two decimal places. Saving and notifications are controlled by flags. The report is based on in-memory state, not existing file contents.

## Expected demonstration output

```text
EMAIL alice@example.test|ORDER|Alice|BOOKx2;PENx3;|109.41
ORDER|Alice|BOOKx2;PENx3;|109.41
EMAIL bob@example.test|ORDER|Bob|BAGx2;|196.80
ORDER|Bob|BAGx2;|196.80
REPORT|2|306.21
```

The saved file contains the two ORDER lines only.

## Your assignment

Refactor this program using Clean Code principles. Keep it small and explain your design decisions.

1. Run the original and identify responsibilities, dependencies, code smells, and likely maintenance risks.
2. Write characterization tests before changing the implementation. Cover the demonstration, student and VIP discounts, coupon stacking, the delivery threshold, reports, and disabled side effects.
3. Replace unclear names, magic numbers, positional data, action codes, and confusing argument lists with meaningful concepts.
4. Separate business calculations from parsing, persistence, presentation, and notifications. Make business rules testable without writing files or printing.
5. Remove unused code and speculative abstractions. Use SOLID where it helps; do not create a class or interface for every operation.
6. Preserve the documented valid-input behavior and output format. Make small changes and keep tests passing.
7. Investigate malformed input, unknown products, zero or negative quantities, invalid customer types, and persistence failures. Record existing behavior. Propose explicit policies and implement them as separately identified behavior changes.
8. Submit the refactored code, tests, and a short explanation mapping important changes to concrete maintenance benefits.

For money, consider decimal arithmetic or integer minor units. Define rounding explicitly and test it; changing rounding policy is a behavior change. The source versions are equivalent for the documented valid-input domain and demonstration, but their runtime parsing and rounding can differ for malformed or extreme inputs.

## Change request after refactoring

Add product MUG (25.00), an EMPLOYEE discount (15%), and a notification implementation that records messages in memory. Explain which modules changed and why. Avoid adding infrastructure unrelated to these requirements.

## Suggested assessment

- Behavior preservation and meaningful tests: 30%.
- Responsibility separation and dependency management: 30%.
- Naming, simplicity, and removal of unnecessary code: 25%.
- Justification and explicit treatment of behavior changes: 15%.

Students should receive this file and their chosen source file. INSTRUCTOR_NOTES.md contains discussion spoilers.
