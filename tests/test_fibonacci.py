"""Tests for utils.math_utils.fibonacci."""

import pytest

from utils.math_utils import fibonacci


class TestFibonacci:
    def test_negative_n_returns_empty_list(self) -> None:
        assert fibonacci(-1) == []

    def test_zero_returns_empty_list(self) -> None:
        assert fibonacci(0) == []

    def test_one_returns_single_element(self) -> None:
        assert fibonacci(1) == [0]

    def test_two_returns_first_two_elements(self) -> None:
        assert fibonacci(2) == [0, 1]

    def test_ten_returns_correct_sequence(self) -> None:
        assert fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_sequence_length_equals_n(self) -> None:
        for n in (1, 5, 10, 20):
            assert len(fibonacci(n)) == n
