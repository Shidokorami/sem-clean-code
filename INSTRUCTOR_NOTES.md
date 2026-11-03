# Instructor notes — intentionally introduced design problems

The exercise is compact (roughly 70–100 lines per language) but combines several independently changing responsibilities. Do not give students a mandatory target class diagram: several small designs can be appropriate.

| Principle or smell | Concrete evidence | Discussion point |
| --- | --- | --- |
| SRP | doIt parses, calculates, updates state, persists, notifies, formats, and reports | Which changes have different reasons to occur? |
| OCP | Product and customer rules require editing conditional chains | A product table may be enough; a strategy hierarchy is not automatically necessary. |
| LSP | Thing advertises refund but always rejects it | If Everything promises refund capability, substituting Thing breaks that expectation. Define the contract before claiming a formal violation. |
| ISP | Everything forces notification, persistence, and refund into one contract | Consumers should depend only on the capability they need. |
| DIP | doIt directly constructs Thing, which hard-codes filesystem and console operations | Inject small collaborators or functions so business logic can be tested independently. |
| YAGNI | Unused mode, currency list, cache, unused argument, and refund capability | These increase mental load without satisfying a current requirement. |
| KISS | One function switches between orders and reports and accepts several flags | Separate clear operations; avoid replacing it with an elaborate framework. |
| Poor naming | doIt, Thing, Everything, a, b, c, z, action | Names should express business meaning. |
| Primitive obsession | Pipe-delimited records, positional indexes, string customer types | Establish a parsing boundary and meaningful data structures. |
| Hidden coupling | Global counters, totals, and cache | Runs influence subsequent calls; isolated tests require state control. |
| Magic numbers | 1, 2, 0.9, 0.95, 12, 100, 1.23, 999 | Separate business policy from implementation details. |
| Error handling debt | Every exception collapses to ERROR | Callers cannot distinguish input errors from storage failures. |
| Consistency debt | State changes before file writing and notification | Failed persistence leaves the order counted; retries can double-count it. |
| Financial debt | Binary floating point, implicit rounding policy | Introduce a defined monetary model without silently changing business rules. |
| Operational debt | Hard-coded relative file path, synchronous append, no durable report state | Discuss the actual scope before adding databases or transactions. |

The cache is written but never read; repeated orders overwrite its email entry. Removing it preserves all documented observable behavior. Unknown products currently cost zero. Negative quantities are accepted. Neither is a desired requirement: have students distinguish refactoring from correcting these behaviors.

The Java interface makes the broad contract explicit. Python and JavaScript use a base class with runtime failures to illustrate the corresponding capability problem. None needs inheritance in the final design.

A useful characterization test sets the discounted subtotal to exactly 100 (e.g. REGULAR, BOOK:2,PEN:4, NONE): no delivery, final amount 123.00. A STUDENT order for BAG:1 with no coupon produces 108.24. An action other than 1 or 2 returns UNKNOWN. A report before any orders returns REPORT|0|0.00.

A useful failure exercise runs with orders.txt pointing to an unwritable target (or uses a failing persistence collaborator after refactoring). Observe that the call returns ERROR while the counter has already advanced. Ask students to propose and document a policy before changing it.

Suggested scope: one extended lab or two shorter labs. Focus on incremental transformations and evidence, not the number of patterns used. A small catalogue, explicit order data, a calculator, and replaceable side-effect collaborators are possible outcomes, not a required solution.
