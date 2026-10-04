from __future__ import annotations
from loguru import logger

from src.calculations.theoretical_solution_solver import REETheoreticalSolver

import pandas as pd

from typing import Callable
# if TYPE_CHECKING:


class DistanceCalculator:
    @staticmethod
    def calculate_distance(
        calculate_distance_function: Callable[..., float],
        theoretical_value: float,
        experimental_values: list[float],
        distance_func_kwargs: dict | None = None,
    ) -> float:
        distance = calculate_distance_function(
            y_true=[theoretical_value for _ in experimental_values],
            y_pred=experimental_values,
            distance_func_kwargs=distance_func_kwargs,
        )
        logger.trace(f"Distance: {distance}")
        return distance

    @staticmethod
    def get_round_distance(
        expected_participant_number: pd.Series,
        standalone_values: pd.Series,
        network_effect: pd.Series,
        price: pd.Series,
        calculate_distance_func: Callable[..., float],
        distance_func_kwargs: dict | None = None,
    ) -> float:
        experimental_values = expected_participant_number.to_list()
        assert isinstance(experimental_values[0], int)
        thetas = standalone_values.to_list()
        thetas.sort()
        assert isinstance(thetas[0], (float, int))
        beta = network_effect.to_list()[0]
        assert isinstance(beta, (float, int))
        price = price.to_list()[0]
        assert isinstance(price, (float, int))
        theoretical_value = REETheoreticalSolver.calculate_theoretical_participant_number(
            thetas=thetas,
            beta=beta,
            price=price,
            is_include_self=True,
        )
        logger.trace(f"Theoretical Value: {theoretical_value}")
        round_distance = DistanceCalculator.calculate_distance(
            calculate_distance_function=calculate_distance_func,
            theoretical_value=theoretical_value,
            experimental_values=experimental_values,
            distance_func_kwargs=distance_func_kwargs,
        )
        logger.debug(f"Round Distance: {round_distance}")
        return round_distance

