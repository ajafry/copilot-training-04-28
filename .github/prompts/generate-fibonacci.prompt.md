---
description: "Generate a Python method that computes the Fibonacci sequence up to n elements, starting from 0. Use when: create fibonacci, generate fibonacci, fibonacci sequence, fibonacci method."
name: "Generate Fibonacci Method"
argument-hint: "Number of elements n (e.g. 10)"
agent: "agent"
---

Create a Python function that computes the Fibonacci sequence up to `$ARGUMENTS` elements, starting from 0.

## Requirements

- Function name: `fibonacci`
- Parameter: `n: int` — the number of elements to return
- Return type: `list[int]`
- The sequence must start from `0` (i.e. `0, 1, 1, 2, 3, 5, ...`)
- Return an empty list when `n <= 0`
- Return `[0]` when `n == 1`

## Code Style

Follow the project conventions in [../../.github/copilot-instructions.md](../../.github/copilot-instructions.md):
- Python 3.13+ syntax and idioms
- PEP 8 formatting
- Type hints on all function signatures and return types
- Add a concise docstring in imperative mood (e.g. "Return the first n elements of the Fibonacci sequence.")
- Use named constants for any magic numbers

## Output

1. The `fibonacci` function added to the appropriate module (or a new `utils/math_utils.py` if no obvious home exists).
2. A corresponding `tests/test_fibonacci.py` with pytest tests covering:
   - `n <= 0` → empty list
   - `n == 1` → `[0]`
   - `n == 2` → `[0, 1]`
   - `n == 10` → `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`
   - Verify the sequence length equals `n`
