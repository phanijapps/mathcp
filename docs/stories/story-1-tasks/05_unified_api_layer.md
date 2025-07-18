# Task 5: Unified API Layer (Internal)

**Description:**
Expose a unified interface for all math functions via the internal API layer.

**Progress Notes:**
- [x] api/dispatcher.py exposes a unified interface for all math functions
- [x] API layer uses only internal Python calls (no REST/MCP yet)
- [x] Example usage can be added in docs or tests

**Next:** Proceed to Task 6: Documentation & Examples

**Acceptance Criteria:**
- [ ] `api/dispatcher.py` exposes a unified interface for all math functions
- [ ] Example: `from math_genius.api import solve_equation, area_of_circle, differentiate`
- [ ] API layer uses only internal Python calls (no REST/MCP yet)
- [ ] Example usage in docs and/or `tests/`


**Notes:**
- Ensure the API layer is ready for future REST/MCP exposure but only supports internal calls for now.

---

## QA Test Cases

- Confirm `api/dispatcher.py` exposes a unified interface for all math functions.
- Test that functions can be imported and used as described (e.g., `from math_genius.api import solve_equation`).
- Ensure the API layer only uses internal Python calls.
- Check for example usage in documentation or tests.
