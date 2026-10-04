from __future__ import annotations
import pytest
from loguru import logger

from src.calculations.distance_function_factory import DistanceFunctionFactory
from src.calculations.distance_calculator import (
    DistanceCalculator,
)

from tests.data.distance_calculator_cases import (
    CALCULATE_DISTANCE_CASES,
)

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestDistanceCalculator:
    @pytest.mark.parametrize(
        'inputs, expected',
        CALCULATE_DISTANCE_CASES,
    )
    def test_calculate_distance(
        self,
        inputs,
        expected,
    ):
        calculate_distance_function = DistanceFunctionFactory.create_distance_function_via_name(
            distance_function_name=inputs['distance_function_name'],
        )
        theoretical_value = inputs['theoretical_value']
        experimental_values = inputs['experimental_values']
        distance_func_kwargs = inputs['distance_func_kwargs']
        distance = DistanceCalculator.calculate_distance(
            calculate_distance_function=calculate_distance_function,
            theoretical_value=theoretical_value,
            experimental_values=experimental_values,
            distance_func_kwargs=distance_func_kwargs,
        )
        logger.debug(f"distance: {distance}")
        assert type(distance) is float

