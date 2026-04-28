"""Math utility functions."""

FIBONACCI_BASE_SEQUENCE = [0, 1]


def fibonacci(n: int) -> list[int]:
    """Return the first n elements of the Fibonacci sequence, starting from 0."""
    if n <= 0:
        return []
    if n == 1:
        return [0]

    sequence = FIBONACCI_BASE_SEQUENCE.copy()
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence
