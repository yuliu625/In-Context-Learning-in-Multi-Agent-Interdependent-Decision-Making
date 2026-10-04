from __future__ import annotations
from loguru import logger

from typing import TYPE_CHECKING, Literal, Callable
# if TYPE_CHECKING:


class UtilityFunctionFactory:
    @staticmethod
    def create_utility_function_via_name(
        utility_function_name: Literal[
            'linear',
        ],
    ) -> Callable:
        if utility_function_name == 'linear':
            return UtilityFunctionFactory.create_linear_utility_function()
        else:
            raise ValueError(f"Unsupported Utility Function: {utility_function_name}")

    @staticmethod
    def create_linear_utility_function():
        def linear_utility_function(
            theta: int,
            beta: float,
            n: int,
            p: float,
        ) -> float:
            return theta + beta * n - p
        logger.debug(f"Create linear utility function.")
        return linear_utility_function

