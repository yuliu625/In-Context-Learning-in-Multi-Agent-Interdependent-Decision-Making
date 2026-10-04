from __future__ import annotations
import pytest

from src.calculations.theoretical_solution_solver import REETheoreticalSolver

from tests.data.theoretical_solution_solver_cases import (
    CALCULATE_THEORETICAL_PRICES_CASES,
    CALCULATE_THEORETICAL_PARTICIPANT_NUMBER_CASES,
)

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestREETheoreticalSolver:
    @pytest.mark.parametrize(
        'inputs, expected',
        CALCULATE_THEORETICAL_PRICES_CASES,
    )
    def test_calculate_theoretical_prices(
        self,
        inputs,
        expected,
    ):
        thetas = inputs['thetas']
        beta = inputs['beta']
        precision = inputs['precision']
        step = inputs['step']
        is_include_self = inputs['is_include_self']
        assert REETheoreticalSolver.calculate_theoretical_prices(
            thetas=thetas,
            beta=beta,
            precision=precision,
            step=step,
            is_include_self=is_include_self,
        ) == expected

    @pytest.mark.parametrize(
        'inputs, expected',
        CALCULATE_THEORETICAL_PARTICIPANT_NUMBER_CASES,
    )
    def test_calculate_theoretical_participant_number(
        self,
        inputs,
        expected,
    ):
        thetas = inputs['thetas']
        beta = inputs['beta']
        price = inputs['price']
        is_include_self = inputs['is_include_self']
        assert REETheoreticalSolver.calculate_theoretical_participant_number(
            thetas=thetas,
            beta=beta,
            price=price,
            is_include_self=is_include_self,
        ) == expected

