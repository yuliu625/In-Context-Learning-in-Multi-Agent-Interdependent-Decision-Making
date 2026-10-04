from __future__ import annotations
from loguru import logger

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


CALCULATE_DISTANCE_CASES = [
    (
        dict(
            distance_function_name='MAE',
            theoretical_value=2.0,
            experimental_values=[1, 2, 4],
            distance_func_kwargs=None,
        ),
        0,
    ),
    (
        dict(
            distance_function_name='MSE',
            theoretical_value=2,
            experimental_values=[1, 2, 4],
            distance_func_kwargs=None,
        ),
        0,
    ),
]

