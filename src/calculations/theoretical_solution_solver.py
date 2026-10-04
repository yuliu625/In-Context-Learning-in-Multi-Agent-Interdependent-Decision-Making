from __future__ import annotations
from loguru import logger

import bisect

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class REETheoreticalSolver:
    @staticmethod
    def calculate_theoretical_prices(
        thetas: list[float],
        beta: float,
        precision: float = 0.01,
        step: int = 1,
        is_include_self: bool = False,
    ) -> list[float]:
        participant_number = len(thetas)
        participant_number_offset = 0 if is_include_self else 1
        theoretical_solution = [
            thetas[i] + beta*(participant_number-i-participant_number_offset) - precision
            for i in range(participant_number)
        ]
        logger.trace(f"Theoretical Prices: {theoretical_solution}")
        return theoretical_solution[::step]

    @staticmethod
    def calculate_theoretical_participant_number(
        thetas: list[float],
        beta: float,
        price: float,
        is_include_self: bool,
    ) -> int:
        theoretical_prices = REETheoreticalSolver.calculate_theoretical_prices(
            thetas=thetas,
            beta=beta,
            precision=0.0,
            step=1,
            is_include_self=is_include_self,
        )
        return len(thetas) - bisect.bisect_right(theoretical_prices, price)

