from __future__ import annotations
from loguru import logger

from src.calculations.utility_calculator import (
    UtilityParamsNameMap,
    UtilityCalculator,
)

import pandas as pd

from typing import TYPE_CHECKING, Callable
# if TYPE_CHECKING:


class UtilityCalculation:
    @staticmethod
    def calculate_real_utility_by_expectation(
        calculate_utility_function: Callable[..., float],
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        df_copy = df.copy()
        df_copy['expected_payoff'] = UtilityCalculator.calculate_utility(
            calculate_utility_function=calculate_utility_function,
            utility_calculating_params_df=df_copy,
            utility_params_name_map=UtilityParamsNameMap(
                theta='standalone_value',
                beta='network_effect',
                n='expected_participant_number',
                p='price',
            )
        )
        logger.trace(f"Calculated Expected Payoff: \n{df_copy}")
        df_copy['choice_by_expected_payoff'] = UtilityCalculator.get_choices_via_expected_payoff(
            expected_payoff_series=df_copy['expected_payoff'],
        )
        logger.trace(f"Calculated Choice by Expected Payoff: \n{df_copy}")
        df_copy['real_participant_number'] = UtilityCalculator.sum_participant_number(
            choices_series=df_copy['choice_by_expected_payoff'],
        )
        logger.trace(f"Calculated Real Participant Number: \n{df_copy}")
        df_copy['real_payoff'] = UtilityCalculator.calculate_utility(
            calculate_utility_function=calculate_utility_function,
            utility_calculating_params_df=df_copy,
            utility_params_name_map=UtilityParamsNameMap(
                theta='standalone_value',
                beta='network_effect',
                n='real_participant_number',
                p='price',
            )
        )
        logger.trace(f"Calculated Real Payoff: \n{df_copy}")
        df_copy['real_payoff'] = UtilityCalculator.mask_no_choice(
            choices_series=df_copy['choice_by_expected_payoff'],
            payoff_series=df_copy['real_payoff'],
        )
        logger.debug(f"Calculated Real Payoff: \n{df_copy}")
        return df_copy

    @staticmethod
    def calculate_utility_by_choice(
        calculate_utility_function: Callable[..., float],
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        df_copy = df.copy()
        df_copy['real_participant_number'] = UtilityCalculator.sum_participant_number(
            choices_series=df_copy['choice_by_expected_payoff'],
        )
        logger.trace(f"Calculated Real Participant Number: \n{df_copy}")
        df_copy['real_payoff'] = UtilityCalculator.calculate_utility(
            calculate_utility_function=calculate_utility_function,
            utility_calculating_params_df=df_copy,
            utility_params_name_map=UtilityParamsNameMap(
                theta='standalone_value',
                beta='network_effect',
                n='real_participant_number',
                p='price',
            )
        )
        logger.debug(f"Calculated Real Payoff: \n{df_copy}")
        return df_copy

