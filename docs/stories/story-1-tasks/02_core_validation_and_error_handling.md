# Task 2: Core Validation & Error Handling

**Description:**
Implement input validation utilities and custom error handling for all math modules.

**Progress Notes:**
- [x] core/validation.py provides input validation utilities (validate_number, validate_numbers)
- [x] core/errors.py defines custom exceptions (MathGeniusError, ValidationError, CalculationError)
- [ ] All modules will import and use these utilities in subsequent tasks

**Next:** Proceed to Task 3: Implement Arithmetic Operations

**Acceptance Criteria:**
- [ ] `core/validation.py` provides input validation utilities for all math modules
- [ ] `core/errors.py` defines custom exceptions for math errors
- [ ] All modules import and use these utilities for input checking


**Notes:**
- Ensure all validation and error handling is reusable and centralized.

---

## QA Test Cases

- Confirm `core/validation.py` provides reusable input validation utilities.
- Verify `core/errors.py` defines custom exceptions for math errors.
- Check that all modules import and use these utilities for input checking.
- Test that invalid inputs are correctly caught and appropriate errors are raised.
