from __future__ import annotations
from loguru import logger

from src.calculations.utility_function_factory import UtilityFunctionFactory
from src.schemas.interaction_protocols import EnvironmentFeedback
from src.schemas.experiment_configs import (
    EnvironmentConfig,
    AgentConfig,
    ExperimentResult,
)
from src.schemas.mas_state import MASState

import pandas as pd
from pydantic import BaseModel, ConfigDict

from typing import TYPE_CHECKING, Callable
# if TYPE_CHECKING:


PROCESS_STATE_CASES = [
    (
        MASState(
            agent_configs=[
                AgentConfig(
                    agent_id='agent_1',
                    standalone_value=1,
                    model_client='openai',
                    model_name='none',
                    model_configs=dict(),
                    is_reasoning=False,
                    system_message_prompt_template_name='none',
                    message_prompt_template_name='none',
                ),
                AgentConfig(
                    agent_id='agent_2',
                    standalone_value=2,
                    model_client='openai',
                    model_name='none',
                    model_configs=dict(),
                    is_reasoning=False,
                    system_message_prompt_template_name='none',
                    message_prompt_template_name='none',
                ),
                AgentConfig(
                    agent_id='agent_3',
                    standalone_value=3,
                    model_client='openai',
                    model_name='none',
                    model_configs=dict(),
                    is_reasoning=False,
                    system_message_prompt_template_name='none',
                    message_prompt_template_name='none',
                ),
                AgentConfig(
                    agent_id='agent_4',
                    standalone_value=4,
                    model_client='openai',
                    model_name='none',
                    model_configs=dict(),
                    is_reasoning=False,
                    system_message_prompt_template_name='none',
                    message_prompt_template_name='none',
                ),
                AgentConfig(
                    agent_id='agent_5',
                    standalone_value=5,
                    model_client='openai',
                    model_name='none',
                    model_configs=dict(),
                    is_reasoning=False,
                    system_message_prompt_template_name='none',
                    message_prompt_template_name='none',
                ),
                AgentConfig(
                    agent_id='agent_6',
                    standalone_value=6,
                    model_client='openai',
                    model_name='none',
                    model_configs=dict(),
                    is_reasoning=False,
                    system_message_prompt_template_name='none',
                    message_prompt_template_name='none',
                ),
            ],
            environment_config=EnvironmentConfig(
                network_effect=0.5,
                prices=[5,],
                utility_function_name='linear',
                schema_pydantic_base_model_name='only-expectation',
                chat_history_length=7,
            ),
            experiment_round=0,
            last_round_structured_outputs=dict(
                agent_1=dict(
                    expected_participant_number=3,
                ),
                agent_2=dict(
                    expected_participant_number=3,
                ),
                agent_3=dict(
                    expected_participant_number=3,
                ),
                agent_4=dict(
                    expected_participant_number=3,
                ),
                agent_5=dict(
                    expected_participant_number=3,
                ),
                agent_6=dict(
                    expected_participant_number=3,
                ),
            ),
        ),
        dict(
            experiment_round=1,
            round_environment_feedbacks=dict(
                agent_1=EnvironmentFeedback(
                    real_participant_number=3,
                    real_payoff=0.0,
                ),
                agent_2=EnvironmentFeedback(
                    real_participant_number=3,
                    real_payoff=0.0,
                ),
                agent_3=EnvironmentFeedback(
                    real_participant_number=3,
                    real_payoff=0.0,
                ),
                agent_4=EnvironmentFeedback(
                    real_participant_number=3,
                    real_payoff=0.5,
                ),
                agent_5=EnvironmentFeedback(
                    real_participant_number=3,
                    real_payoff=1.5,
                ),
                agent_6=EnvironmentFeedback(
                    real_participant_number=3,
                    real_payoff=2.5,
                ),
            ),
            results=[
                ExperimentResult(
                    experiment_round=0,
                    agent_id='agent_1',
                    standalone_value=1.0,
                    network_effect=0.5,
                    price=5.0,
                    expected_participant_number=3,
                    expected_payoff=-2.5,
                    choice_by_expected_payoff=False,
                    real_participant_number=3,
                    real_payoff=0.0
                ),
                ExperimentResult(
                    experiment_round=0,
                    agent_id='agent_2',
                    standalone_value=2.0,
                    network_effect=0.5,
                    price=5.0,
                    expected_participant_number=3,
                    expected_payoff=-1.5,
                    choice_by_expected_payoff=False,
                    real_participant_number=3,
                    real_payoff=0.0
                ),
                ExperimentResult(
                    experiment_round=0,
                    agent_id='agent_3',
                    standalone_value=3.0,
                    network_effect=0.5,
                    price=5.0,
                    expected_participant_number=3,
                    expected_payoff=-0.5,
                    choice_by_expected_payoff=False,
                    real_participant_number=3,
                    real_payoff=0.0
                ),
                ExperimentResult(
                    experiment_round=0,
                    agent_id='agent_4',
                    standalone_value=4.0,
                    network_effect=0.5,
                    price=5.0,
                    expected_participant_number=3,
                    expected_payoff=0.5,
                    choice_by_expected_payoff=True,
                    real_participant_number=3,
                    real_payoff=0.5
                ),
                ExperimentResult(
                    experiment_round=0,
                    agent_id='agent_5',
                    standalone_value=5.0,
                    network_effect=0.5,
                    price=5.0,
                    expected_participant_number=3,
                    expected_payoff=1.5,
                    choice_by_expected_payoff=True,
                    real_participant_number=3,
                    real_payoff=1.5
                ),
                ExperimentResult(
                    experiment_round=0,
                    agent_id='agent_6',
                    standalone_value=6.0,
                    network_effect=0.5,
                    price=5.0,
                    expected_participant_number=3,
                    expected_payoff=2.5,
                    choice_by_expected_payoff=True,
                    real_participant_number=3,
                    real_payoff=2.5
                ),
            ],
        ),
    ),
]


COLLECT_AGENT_ACTION_DF_CASES = [
    (
        dict(
            agent_config=pd.DataFrame([
                dict(agent_id='agent_1', standalone_value=1,),
                dict(agent_id='agent_2', standalone_value=2,),
                dict(agent_id='agent_3', standalone_value=3,),
                dict(agent_id='agent_4', standalone_value=4,),
                dict(agent_id='agent_5', standalone_value=5,),
                dict(agent_id='agent_6', standalone_value=6,),
            ]),
            network_effect=0.5,
            price=5,
            last_round_structured_outputs=dict(
                agent_1=dict(expected_participant_number=3,),
                agent_2=dict(expected_participant_number=3,),
                agent_3=dict(expected_participant_number=3,),
                agent_4=dict(expected_participant_number=3,),
                agent_5=dict(expected_participant_number=3,),
                agent_6=dict(expected_participant_number=3,),
            ),
        ),
        pd.DataFrame([
            dict(agent_id='agent_1', standalone_value=1, network_effect=0.5, price=5, expected_participant_number=3,),
            dict(agent_id='agent_2', standalone_value=2, network_effect=0.5, price=5, expected_participant_number=3,),
            dict(agent_id='agent_3', standalone_value=3, network_effect=0.5, price=5, expected_participant_number=3,),
            dict(agent_id='agent_4', standalone_value=4, network_effect=0.5, price=5, expected_participant_number=3,),
            dict(agent_id='agent_5', standalone_value=5, network_effect=0.5, price=5, expected_participant_number=3,),
            dict(agent_id='agent_6', standalone_value=6, network_effect=0.5, price=5, expected_participant_number=3,),
        ]),
    ),
]


CALCULATE_ENVIRONMENT_FEEDBACK_DF_CASES = [
    (
        pd.DataFrame({
            'agent_id': ['agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5', 'agent_6'],
            'standalone_value': [1, 2, 3, 4, 5, 6],
            'network_effect': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'expected_participant_number': [3, 3, 3, 3, 3, 3],
            'price': [5, 5, 5, 5, 5, 5],
        }),
        pd.DataFrame({
            'agent_id': ['agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5', 'agent_6'],
            'standalone_value': [1, 2, 3, 4, 5, 6],
            'network_effect': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'expected_participant_number': [3, 3, 3, 3, 3, 3],
            'price': [5, 5, 5, 5, 5, 5],
            'expected_payoff': [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5],
            'choice_by_expected_payoff': [False, False, False, True, True, True],
            'real_participant_number': [3, 3, 3, 3, 3, 3],
            'real_payoff': [0, 0, 0, 0.5, 1.5, 2.5],
        }),
    ),
]


MAKE_ENVIRONMENT_FEEDBACKS_CASES = [
    (
        pd.DataFrame({
            'agent_id': ['agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5', 'agent_6'],
            'standalone_value': [1, 2, 3, 4, 5, 6],
            'network_effect': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'expected_participant_number': [3, 3, 3, 3, 3, 3],
            'price': [5, 5, 5, 5, 5, 5],
            'expected_payoff': [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5],
            'choice_by_expected_payoff': [False, False, False, True, True, True],
            'real_participant_number': [3, 3, 3, 3, 3, 3],
            'real_payoff': [0, 0, 0, 0.5, 1.5, 2.5],
        }),
        dict(
            agent_1=EnvironmentFeedback(real_participant_number=3, real_payoff=0,),
            agent_2=EnvironmentFeedback(real_participant_number=3, real_payoff=0,),
            agent_3=EnvironmentFeedback(real_participant_number=3, real_payoff=0,),
            agent_4=EnvironmentFeedback(real_participant_number=3, real_payoff=0.5,),
            agent_5=EnvironmentFeedback(real_participant_number=3, real_payoff=1.5,),
            agent_6=EnvironmentFeedback(real_participant_number=3, real_payoff=2.5,),
        ),
    ),
]


UPDATE_RESULTS_DF_CASES = [
    (
        dict(
            experiment_round=0,
            round_environment_feedback_df=pd.DataFrame({
                'standalone_value': [1, 2, 3, 4, 5, 6],
                'network_effect': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                'expected_participant_number': [3, 3, 3, 3, 3, 3],
                'price': [5, 5, 5, 5, 5, 5],
                'expected_payoff': [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5],
                'choice_by_expected_payoff': [False, False, False, True, True, True],
                'real_participant_number': [3, 3, 3, 3, 3, 3],
                'real_payoff': [0, 0, 0, 0.5, 1.5, 2.5],
            }),
            results_df=pd.DataFrame(),
        ),
        pd.DataFrame({
            'experiment_round': [0, 0, 0, 0, 0, 0],
            'standalone_value': [1, 2, 3, 4, 5, 6],
            'network_effect': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'expected_participant_number': [3, 3, 3, 3, 3, 3],
            'price': [5, 5, 5, 5, 5, 5],
            'expected_payoff': [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5],
            'choice_by_expected_payoff': [False, False, False, True, True, True],
            'real_participant_number': [3, 3, 3, 3, 3, 3],
            'real_payoff': [0, 0, 0, 0.5, 1.5, 2.5],
        }),
    ),
]

