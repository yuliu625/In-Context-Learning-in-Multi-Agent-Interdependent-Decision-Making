from __future__ import annotations
import pytest

from src.calculations.utility_function_factory import UtilityFunctionFactory
from src.calculations.utility_calculation import UtilityCalculation

from tests.data.utility_calculation_cases import (
    CALCULATE_REAL_UTILITY_BY_EXPECTATION_CASES,
)

from pandas.testing import assert_frame_equal

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestUtilityCalculationMethods:
    @pytest.mark.parametrize(
        'inputs, expected',
        CALCULATE_REAL_UTILITY_BY_EXPECTATION_CASES,
    )
    def test_calculate_real_utility_by_expectation(
        self,
        inputs,
        expected,
    ):
        assert_frame_equal(
            UtilityCalculation.calculate_real_utility_by_expectation(
                calculate_utility_function=UtilityFunctionFactory.create_linear_utility_function(),
                df=inputs,
            ),
            expected,
        )

