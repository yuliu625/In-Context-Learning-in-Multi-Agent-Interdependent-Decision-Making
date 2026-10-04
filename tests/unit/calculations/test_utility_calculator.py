from __future__ import annotations
import pytest

from src.calculations.utility_function_factory import UtilityFunctionFactory
from src.calculations.utility_calculator import UtilityCalculator

from tests.data.utility_calculating_cases import (
    SUM_PARTICIPANT_NUMBER_CASES,
    GET_CHOICES_BY_EXPECTED_PAYOFF_CASES,
    CALCULATE_UTILITY_CASES,
    MASK_NO_CHOICE_CASES,
)

from pandas.testing import assert_series_equal

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestUtilityCalculator:
    @pytest.mark.parametrize(
        'inputs, expected',
        SUM_PARTICIPANT_NUMBER_CASES,
    )
    def test_sum_participant_number(
        self,
        inputs,
        expected,
    ):
        assert_series_equal(
            UtilityCalculator.sum_participant_number(inputs),
            expected,
        )

    @pytest.mark.parametrize(
        'inputs, expected',
        GET_CHOICES_BY_EXPECTED_PAYOFF_CASES,
    )
    def test_get_choices_by_expected_payoff(
        self,
        inputs,
        expected,
    ):
        assert_series_equal(
            UtilityCalculator.get_choices_via_expected_payoff(inputs),
            expected,
        )

    @pytest.mark.parametrize(
        'inputs, expected',
        CALCULATE_UTILITY_CASES,
    )
    def test_calculate_utility(
        self,
        inputs,
        expected,
    ):
        utility_calculating_params_df = inputs['utility_calculating_params_df']
        utility_params_name_map = inputs['utility_params_name_map']
        assert_series_equal(
            UtilityCalculator.calculate_utility(
                calculate_utility_function=UtilityFunctionFactory.create_linear_utility_function(),
                utility_calculating_params_df=utility_calculating_params_df,
                utility_params_name_map=utility_params_name_map,
            ),
            expected,
        )

    @pytest.mark.parametrize(
        'inputs, expected',
        MASK_NO_CHOICE_CASES,
    )
    def test_mask_no_choice(
        self,
        inputs,
        expected,
    ):
        choice_series = inputs['choice_series']
        payoff_series = inputs['payoff_series']
        assert_series_equal(
            UtilityCalculator.mask_no_choice(
                choices_series=choice_series,
                payoff_series=payoff_series,
            ),
            expected,
        )

