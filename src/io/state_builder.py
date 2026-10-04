from __future__ import annotations
from loguru import logger

from src.schemas.mas_state import MASState
from src.schemas.structured_output_format import StructuredOutputFormatFactory
from src.calculations.utility_function_factory import UtilityFunctionFactory

from typing import TYPE_CHECKING, Literal, Callable
if TYPE_CHECKING:
    from src.schemas.experiment_configs import (
        EnvironmentConfig,
        AgentConfig,
        ExperimentResult,
    )
    from langchain_core.messages import AnyMessage
    import pandas as pd
    from pydantic import BaseModel


class StateBuilder:
    @staticmethod
    def build_mas_state(
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
        chat_histories: dict[str, list[AnyMessage]] | None,
        results: list[ExperimentResult] | None,
    ) -> MASState:
        if chat_histories is None:
            chat_histories = {}
        if results is None:
            results = []
        mas_state = MASState(
            environment_config=environment_config,
            agent_configs=agent_configs,
            experiment_round=0,
            chat_histories=chat_histories,
            results=results,
        )
        logger.debug(f"Built MAS State: {mas_state}")
        return mas_state

    @staticmethod
    def get_agent_configs(
        agent_configs_df: pd.DataFrame,
    ) -> list[AgentConfig]:
        agent_configs = []
        for _, row in agent_configs_df.iterrows():
            agent_config = AgentConfig(
                agent_id=row['agent_id'],
                model_client=row['model_client'],
                model_name=row['model_name'],
                is_reasoning=row['is_reasoning'],
                model_configs=dict(
                    temperature=round(row['temperature'], 1),
                    top_p=round(row['top_p'], 1),
                ),
                standalone_value=row['standalone_value'],
                system_message_prompt_template_name=row['system_message_prompt_template_name'],
                message_prompt_template_name=row['message_prompt_template_name'],
            )
            agent_configs.append(agent_config)
        return agent_configs

    @staticmethod
    def get_utility_function(
        utility_function_name: Literal['linear'],
    ) -> Callable[..., float]:
        utility_function = UtilityFunctionFactory.create_utility_function_via_name(
            utility_function_name=utility_function_name,
        )
        return utility_function

    @staticmethod
    def get_schema_pydantic_base_model(
        schema_pydantic_base_model_name: Literal[
            'all', 'only-expectation', 'only-choice',
        ],
    ) -> type[BaseModel]:
        schema_pydantic_base_model = StructuredOutputFormatFactory.create_structured_output_format(
            schema_pydantic_base_model_name=schema_pydantic_base_model_name,
        )
        return schema_pydantic_base_model

