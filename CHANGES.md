## 1. Decomposition of doIt function
**Change**: `doIt` function was decomposed to several other classes and functions.
**Rationale**: This function handled too many responsibilities, being an instance of the *God function*. We decomposed it to functions and classes that all have their specific responsibility. Classes were used in cases of functionalities  that seemed to be related.

## 2. Variables Names changed
**Change**: Names of nearly all the variables used in program has changed.
**Rationale**: Previously used names didn't provide necessary information to identify purpose of the variables, which made code harder to understand. Execution of this change followed PEP8 which standardize conventions used in Python language.

## 3. Removal of the obsolete code
**Change**: Removed unused code such as Parent Class without reason to exist, code left for the future.
**Rationale**: This parts of code didn't provide any necessary function to the code. In case of some variables we followed YAGNI principle (future currencies).

## 4. Introduction of order data models
**Change**: We introduced DTO to the code.
**Rationale**: By using DTO as our data model we introduced form of contract to functions and methods. This makes following the data transported between different parts of code easier and increases maintainability.

## 5. Creating Enums and dictionaries for data
**Change**: We added Enumerations for types of clients, dictionaries for Product Prices.
**Rationale**: Usage of Enums allows to reduce amount of duplicate code and problems related with different naming of the same domain objects. Usage of dictionaries creates simple mapping of product to its price, customers types to their discounts etc. Both of these changes ake the system easier to extend by updating clearly defined data structures instead of modifying conditional statements in code logic.

## 6. Usage of Constants
**Change**: We introduced constants for Magic Numbers and names from domain.
**Rationale**: By usage of constants we centralized so-called *Magic numbers*, which represent values related to the domain such as delivery fee or tax rate. This prevents inconsistencies between different fragments of the code, by making sure all of them refer to the same value. Additionally, it increases maintainability - change in one of this values would result in only change value onf the constant, instead of searching all the usage in the code. 

## 7. Change of the exceptions
**Change**: We introduced different types of exceptions and provided description for them.
**Rationale**: Previously, the program used a broad exception handler that hid the actual causes of errors. By introducing custom exceptions and more specific error handling, we improved error identification, debugging, and maintainability. This also follows the Clean Code principle of providing meaningful error information.

## 8. Validation
**Change**: We added validation to function and methods.
**Rationale**: It prevents insertion of incorrect data to the system, which would result in unexcepted behaviour. For example, the program now validates whether the quantity of each ordered product is greater than zero.

## 9. Usage of Decimal Type
**Change**: Use of Decimal in variables representing fractional values.
**Rationale**: Decimal provides developers with type that is resilient to floating-point error.

## 10. Separation of files
**Change**: We partitioned code into the different files.
**Rationale**: It increases ability to navigate in code, improves importing by grouping related functions in the same file.

## 11. Type hints
**Change**: We added types hints for functions, methods, parameters and some variables.
**Rationale**: Despite python being dynamically typed language, usage of type hints allow developers to easily understand what type of data is represented by variables and what type is expected to be returned.

## 12. Removal of global variables
**Change**: Global variables were replaced with local variables in classes.
**Rationale**: By encapsulating the state within a class, each processor instance can manage its own data independently. 

## 13. Introduction of Dependency Injection
**Change**: We introduced dependency injection into OrderProcessor, allowing the price calculator, formatter, order saver, and notification handler to be provided as dependencies.
**Rationale**: Dependency injection reduces coupling between components and makes them easier to replace or test independently.