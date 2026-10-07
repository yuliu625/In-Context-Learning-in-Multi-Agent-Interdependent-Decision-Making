from __future__ import annotations
from loguru import logger

from src.schemas.interaction_protocols import EnvironmentFeedback
from src.schemas.calculation_fields import ExperimentResult
from src.calculations.utility_calculation import UtilityCalculation

import inspect
import pandas as pd

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from src.schemas.mas_state import MASState
    from langchain_core.runnables import RunnableConfig


class ResultCollector:
    def __init__(
        self,
        utility_function: Callable[..., float],
    ):
        self.utility_function = utility_function
        logger.debug(f"Set result_collector's utility_function: {inspect.getsource(utility_function)}")

    def process_state(
        self,
        state: MASState,
        config: RunnableConfig,
    ) -> dict:
        agent_action_df = ResultCollector.collect_agent_action_df(
            agent_configs_df=state.agent_configs_df,
            network_effect=state.environment_config.network_effect,
            price=state.environment_config.prices[state.experiment_round],
            last_round_structured_outputs=state.last_round_structured_outputs,
        )
        environment_feedback_df = ResultCollector.calculate_environment_feedback_df(
            agent_action_df=agent_action_df,
            utility_function=self.utility_function,
        )
        environment_feedbacks = ResultCollector.make_environment_feedbacks(
            environment_feedback_df=environment_feedback_df,
        )
        results = ResultCollector.update_results(
            experiment_round=state.experiment_round,
            round_environment_feedback_df=environment_feedback_df,
            results=state.results,
        )
        logger.info(f"Round {state.experiment_round} End.")
        fields_to_update = dict(
            experiment_round=state.experiment_round+1,
            round_environment_feedbacks=environment_feedbacks,
            results=results,
        )
        logger.debug(f"Update Fields: {fields_to_update}")
        return fields_to_update

    @staticmethod
    def collect_agent_action_df(
        agent_configs_df: pd.DataFrame,
        network_effect: float,
        price: float,
        last_round_structured_outputs: dict[str, dict],
    ) -> pd.DataFrame:
        agent_action_list = []
        for index, row in agent_configs_df.iterrows():
            agent_id = row['agent_id']
            agent_action = dict(
                agent_id=agent_id,
                standalone_value=row['standalone_value'],
                network_effect=network_effect,
                price=price,
                expected_participant_number=last_round_structured_outputs[agent_id].get(
                    'expected_participant_number', ''
                ),
            )
            agent_action_list.append(agent_action)
        agent_action_df = pd.DataFrame(agent_action_list)
        logger.trace(f"agent_action_df: {agent_action_df}")
        return agent_action_df

    @staticmethod
    def calculate_environment_feedback_df(
        agent_action_df: pd.DataFrame,
        utility_function: Callable,
    ) -> pd.DataFrame:
        environment_feedback_df = UtilityCalculation.calculate_real_utility_by_expectation(
            calculate_utility_function=utility_function,
            df=agent_action_df,
        )
        logger.trace(f"environment_feedback_df: {environment_feedback_df}")
        return environment_feedback_df

    @staticmethod
    def make_environment_feedbacks(
        environment_feedback_df: pd.DataFrame,
    ) -> dict[str, EnvironmentFeedback]:
        environment_feedbacks = {}
        for index, row in environment_feedback_df.iterrows():
            agent_id = row['agent_id']
            real_participant_number = row['real_participant_number']
            real_payoff = row['real_payoff']
            environment_feedbacks[agent_id] = EnvironmentFeedback(
                real_participant_number=real_participant_number,
                real_payoff=round(real_payoff, 2),
            )
        logger.trace(f"environment_feedbacks: {environment_feedbacks}")
        return environment_feedbacks

    @staticmethod
    def update_results_df(
        experiment_round: int,
        round_environment_feedback_df: pd.DataFrame,
        results_df: pd.DataFrame,
    ) -> pd.DataFrame:
        round_environment_feedback_df_ = round_environment_feedback_df.copy()
        results_df_ = results_df.copy()
        round_environment_feedback_df_['experiment_round'] = experiment_round
        return pd.concat(
            [results_df_, round_environment_feedback_df_],
            axis=0,
            ignore_index=True,
        )

    @staticmethod
    def update_results(
        experiment_round: int,
        round_environment_feedback_df: pd.DataFrame,
        results: list[ExperimentResult],
    ) -> list[ExperimentResult]:
        results_ = results.copy()
        for _, row in round_environment_feedback_df.iterrows():
            result = ExperimentResult(
                experiment_round=experiment_round,
                agent_id=row['agent_id'],
                standalone_value=row['standalone_value'],
                network_effect=row['network_effect'],
                price=row['price'],
                expected_participant_number=row['expected_participant_number'],
                expected_payoff=row['expected_payoff'],
                choice_by_expected_payoff=row['choice_by_expected_payoff'],
                real_participant_number=row['real_participant_number'],
                real_payoff=row['real_payoff'],
            )
            results_.append(result)
        logger.trace(f"results: {results_}")
        return results_

