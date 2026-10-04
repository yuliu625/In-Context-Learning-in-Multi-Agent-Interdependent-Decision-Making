from __future__ import annotations
from loguru import logger

from src.calculations.distance_calculator import DistanceCalculator

import pandas as pd

from typing import TYPE_CHECKING, Callable
# if TYPE_CHECKING:


class DistanceCalculation:
    @staticmethod
    def calculate_experiment_distances(
        df: pd.DataFrame,
        calculate_distance_func: Callable[..., float],
        calculate_distance_func_kwargs: dict | None = None,
    ) -> dict:
        df_copy = df.copy()
        experiment_round: list[int] = df_copy['experiment_round'].unique().tolist()
        distances = {}
        for experiment_round_idx in experiment_round:
            round_df = df_copy[df_copy['experiment_round'] == experiment_round_idx]
            standalone_values = round_df['standalone_value']
            network_effect = round_df['network_effect']
            prices = round_df['price']
            expected_participant_number = round_df['expected_participant_number']
            round_distance = DistanceCalculator.get_round_distance(
                expected_participant_number=expected_participant_number,
                standalone_values=standalone_values,
                network_effect=network_effect,
                price=prices,
                calculate_distance_func=calculate_distance_func,
                distance_func_kwargs=calculate_distance_func_kwargs,
            )
            distances[experiment_round_idx] = round_distance
        logger.debug(f"Distances: {distances}")
        return distances

    @staticmethod
    def calculate_experiment_distances_with_price(
        df: pd.DataFrame,
        calculate_distance_func: Callable[..., float],
        calculate_distance_func_kwargs: dict | None = None,
    ) -> dict:
        df_copy = df.copy()
        experiment_round: list[int] = df_copy['experiment_round'].unique().tolist()
        distances = {}
        for experiment_round_idx in experiment_round:
            round_df = df_copy[df_copy['experiment_round'] == experiment_round_idx]
            standalone_values = round_df['standalone_value']
            network_effect = round_df['network_effect']
            prices = round_df['price']
            expected_participant_number = round_df['expected_participant_number']
            round_distance = DistanceCalculator.get_round_distance(
                expected_participant_number=expected_participant_number,
                standalone_values=standalone_values,
                network_effect=network_effect,
                price=prices,
                calculate_distance_func=calculate_distance_func,
                distance_func_kwargs=calculate_distance_func_kwargs,
            )
            distances[prices.to_list()[0]] = round_distance
        logger.debug(f"Distances: {distances}")
        return distances

