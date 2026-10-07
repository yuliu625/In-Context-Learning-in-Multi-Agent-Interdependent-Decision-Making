from __future__ import annotations
import pytest

from src.fsm.nodes.result_collector import ResultCollector
from src.calculations.utility_function_factory import UtilityFunctionFactory
from tests.data.result_collector_cases import (
    PROCESS_STATE_CASES,
    COLLECT_AGENT_ACTION_DF_CASES,
    CALCULATE_ENVIRONMENT_FEEDBACK_DF_CASES,
    MAKE_ENVIRONMENT_FEEDBACKS_CASES,
    UPDATE_RESULTS_DF_CASES,
)

from pandas.testing import assert_frame_equal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.mas_state import MASState
    import pandas as pd


class TestResultCollector:
    @pytest.mark.parametrize(
        'inputs, expected', PROCESS_STATE_CASES,
    )
    def test_process_state(
        self,
        inputs: MASState,
        expected: dict,
    ):
        result_collector = ResultCollector(
            utility_function=UtilityFunctionFactory.create_utility_function_via_name(
                utility_function_name=inputs.environment_config.utility_function_name,
            ),
        )
        state = result_collector.process_state(
            state=inputs,
            config=None,
        )
        assert state['experiment_round'] == expected['experiment_round']
        assert state['round_environment_feedbacks'] == expected['round_environment_feedbacks']
        assert state['results'] == expected['results']

    @pytest.mark.parametrize(
        'inputs, expected', COLLECT_AGENT_ACTION_DF_CASES,
    )
    def test_collect_agent_action_df(
        self,
        inputs: dict,
        expected: pd.DataFrame,
    ):
        agent_config = inputs['agent_config']
        network_effect = inputs['network_effect']
        price = inputs['price']
        last_round_structured_outputs = inputs['last_round_structured_outputs']
        agent_action_df = ResultCollector.collect_agent_action_df(
                agent_configs_df=agent_config,
                network_effect=network_effect,
                price=price,
                last_round_structured_outputs=last_round_structured_outputs,
            )
        assert_frame_equal(
            agent_action_df,
            expected,
        )

    @pytest.mark.parametrize(
        'inputs, expected', CALCULATE_ENVIRONMENT_FEEDBACK_DF_CASES,
    )
    def test_calculate_environment_feedback_df(
        self,
        inputs: pd.DataFrame,
        expected: pd.DataFrame,
    ):
        environment_feedback_df = ResultCollector.calculate_environment_feedback_df(
                agent_action_df=inputs,
                utility_function=UtilityFunctionFactory.create_linear_utility_function()
            )
        assert_frame_equal(
            environment_feedback_df,
            expected,
        )

    @pytest.mark.parametrize(
        'inputs, expected', MAKE_ENVIRONMENT_FEEDBACKS_CASES,
    )
    def test_make_environment_feedbacks(
        self,
        inputs: pd.DataFrame,
        expected: dict,
    ):
        environment_feedbacks = ResultCollector.make_environment_feedbacks(
            environment_feedback_df=inputs,
        )
        assert environment_feedbacks == expected

    @pytest.mark.parametrize(
        'inputs, expected', UPDATE_RESULTS_DF_CASES,
    )
    def test_update_results_df(
        self,
        inputs: dict,
        expected: pd.DataFrame,
    ):
        experiment_round = inputs['experiment_round']
        round_environment_feedback_df = inputs['round_environment_feedback_df']
        results_df = inputs['results_df']
        assert_frame_equal(
            ResultCollector.update_results_df(
                experiment_round=experiment_round,
                round_environment_feedback_df=round_environment_feedback_df,
                results_df=results_df,
            ),
            expected,
            check_like=True,
        )

