from __future__ import annotations
from loguru import logger

import pandas as pd
from pandas.core.dtypes.common import (
    is_bool_dtype,
    is_numeric_dtype,
)
from pydantic import BaseModel, Field

from typing import TYPE_CHECKING, Callable, Literal
# if TYPE_CHECKING:


class UtilityParamsNameMap(BaseModel):
    theta: str = Field(
        ...,
    )
    beta: str = Field(
        ...,
    )
    n: str = Field(
        ...,
    )
    p: str = Field(
        ...,
    )


class UtilityCalculator:
    @staticmethod
    def calculate_utility(
        calculate_utility_function: Callable[..., float],
        utility_calculating_params_df: pd.DataFrame,
        utility_params_name_map: UtilityParamsNameMap,
    ) -> pd.Series:
        def calculate_expectation_utility(
            row: pd.Series,
            utility_params_name_map_: UtilityParamsNameMap,
        ) -> float:
            return calculate_utility_function(
                theta=row[utility_params_name_map_.theta],
                beta=row[utility_params_name_map_.beta],
                n=row[utility_params_name_map_.n],
                p=row[utility_params_name_map_.p],
            )
        utility_series =  utility_calculating_params_df.apply(
            lambda row: calculate_expectation_utility(row, utility_params_name_map),
            axis=1,
        )
        logger.trace(f"Utility Series: \n{utility_series}")
        return utility_series

    @staticmethod
    def get_choices_via_expected_payoff(
        expected_payoff_series: pd.Series,
    ) -> pd.Series:
        def is_positive_payoff(payoff: float) -> bool:
            return payoff > 0
        assert is_numeric_dtype(expected_payoff_series)
        choices_series = expected_payoff_series.apply(is_positive_payoff)
        logger.trace(f"Choices Series: \n{choices_series}")
        return choices_series

    @staticmethod
    def sum_participant_number(
        choices_series: pd.Series,
    ) -> pd.Series:
        assert is_bool_dtype(choices_series)
        participant_number = choices_series.sum()
        assert is_numeric_dtype(participant_number)
        participant_number_series =  pd.Series(
            data=[participant_number] * len(choices_series),
            index=choices_series.index,
        )
        logger.trace(f"Participant Number Series: \n{participant_number_series}")
        return participant_number_series

    @staticmethod
    def mask_no_choice(
        choices_series: pd.Series,
        payoff_series: pd.Series,
    ) -> pd.Series:
        assert is_bool_dtype(choices_series)
        assert is_numeric_dtype(payoff_series)
        result = payoff_series.copy()
        result[~choices_series] = 0
        logger.trace(f"Mask No Choice Result Series: \n{result}")
        return result

