"""Tests for the calculator module."""

import types
from unittest.mock import patch

import pytest

from views.calculator import (
    ALLOWED_CHARS,
    OPERATOR_MAP,
    _append,
    _backspace,
    _clear,
    _evaluate,
)


@pytest.fixture
def session_state():
    """Provide a fresh session state mock for each test."""
    state = types.SimpleNamespace(calc_expr="", calc_result="")
    with patch("views.calculator.st") as mock_st:
        mock_st.session_state = state
        yield state


class TestAppend:
    def test_appends_value_to_expression(self, session_state) -> None:
        _append("5")
        assert session_state.calc_expr == "5"

    def test_appends_multiple_values_sequentially(self, session_state) -> None:
        _append("1")
        _append("+")
        _append("2")
        assert session_state.calc_expr == "1+2"

    def test_clears_result_on_append(self, session_state) -> None:
        session_state.calc_result = "10"
        _append("5")
        assert session_state.calc_result == ""


class TestClear:
    def test_clears_expression(self, session_state) -> None:
        session_state.calc_expr = "1+2"
        _clear()
        assert session_state.calc_expr == ""

    def test_clears_result(self, session_state) -> None:
        session_state.calc_result = "3"
        _clear()
        assert session_state.calc_result == ""

    def test_clears_both_simultaneously(self, session_state) -> None:
        session_state.calc_expr = "7*8"
        session_state.calc_result = "56"
        _clear()
        assert session_state.calc_expr == ""
        assert session_state.calc_result == ""


class TestBackspace:
    def test_removes_last_character(self, session_state) -> None:
        session_state.calc_expr = "123"
        _backspace()
        assert session_state.calc_expr == "12"

    def test_empty_expression_stays_empty(self, session_state) -> None:
        session_state.calc_expr = ""
        _backspace()
        assert session_state.calc_expr == ""

    def test_single_character_becomes_empty(self, session_state) -> None:
        session_state.calc_expr = "5"
        _backspace()
        assert session_state.calc_expr == ""

    def test_clears_result_on_backspace(self, session_state) -> None:
        session_state.calc_expr = "5"
        session_state.calc_result = "5"
        _backspace()
        assert session_state.calc_result == ""


class TestEvaluate:
    def test_evaluates_addition(self, session_state) -> None:
        session_state.calc_expr = "1+2"
        _evaluate()
        assert session_state.calc_result == "3"

    def test_evaluates_subtraction(self, session_state) -> None:
        session_state.calc_expr = "10-4"
        _evaluate()
        assert session_state.calc_result == "6"

    def test_evaluates_multiplication(self, session_state) -> None:
        session_state.calc_expr = "3*4"
        _evaluate()
        assert session_state.calc_result == "12"

    def test_evaluates_division(self, session_state) -> None:
        session_state.calc_expr = "10/2"
        _evaluate()
        assert session_state.calc_result == "5.0"

    def test_evaluates_complex_expression(self, session_state) -> None:
        session_state.calc_expr = "(1+2)*3"
        _evaluate()
        assert session_state.calc_result == "9"

    def test_empty_expression_sets_error(self, session_state) -> None:
        session_state.calc_expr = ""
        _evaluate()
        assert session_state.calc_result == "Error"

    def test_disallowed_characters_set_error(self, session_state) -> None:
        session_state.calc_expr = "1+a"
        _evaluate()
        assert session_state.calc_result == "Error"

    def test_invalid_syntax_sets_error(self, session_state) -> None:
        session_state.calc_expr = "1+"
        _evaluate()
        assert session_state.calc_result == "Error"

    def test_division_by_zero_sets_error(self, session_state) -> None:
        session_state.calc_expr = "1/0"
        _evaluate()
        assert session_state.calc_result == "Error"

    def test_float_arithmetic(self, session_state) -> None:
        session_state.calc_expr = "1.5+2.5"
        _evaluate()
        assert session_state.calc_result == "4.0"

    def test_chained_addition_without_parentheses(self, session_state) -> None:
        session_state.calc_expr = "1+2+3"
        _evaluate()
        assert session_state.calc_result == "6"

    def test_multiplication_before_addition_without_parentheses(self, session_state) -> None:
        session_state.calc_expr = "3*2+1"
        _evaluate()
        assert session_state.calc_result == "7"


class TestConstants:
    def test_allowed_chars_contains_digits(self) -> None:
        for digit in "0123456789":
            assert digit in ALLOWED_CHARS

    def test_allowed_chars_contains_arithmetic_operators(self) -> None:
        for op in "+-*/.":
            assert op in ALLOWED_CHARS

    def test_allowed_chars_contains_parentheses(self) -> None:
        assert "(" in ALLOWED_CHARS
        assert ")" in ALLOWED_CHARS

    def test_allowed_chars_excludes_letters(self) -> None:
        for letter in "abcdefghijklmnopqrstuvwxyz":
            assert letter not in ALLOWED_CHARS

    def test_operator_map_division(self) -> None:
        assert OPERATOR_MAP["÷"] == "/"

    def test_operator_map_multiplication(self) -> None:
        assert OPERATOR_MAP["×"] == "*"

    def test_operator_map_subtraction(self) -> None:
        assert OPERATOR_MAP["−"] == "-"
