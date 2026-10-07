from __future__ import annotations
from loguru import logger

from src.calculations.utility_function_factory import UtilityFunctionFactory
from src.prompts.prompt_template_factories import ParticipantPromptTemplateFactory
from src.schemas.structured_output_format import StructuredOutputFormatFactory

from typing import TYPE_CHECKING, Literal, Callable
if TYPE_CHECKING:
    from src.schemas.experiment_configs import (
        EnvironmentConfig,
        AgentConfig,
    )
    from langchain_core.prompts import HumanMessagePromptTemplate
    from pydantic import BaseModel
    import pandas as pd


class NodeBuildingTools:
    @staticmethod
    def get_utility_function(
        utility_function_name: Literal[
            'linear',
        ],
    ) -> Callable[..., float]:
        return UtilityFunctionFactory.create_utility_function_via_name(
            utility_function_name=utility_function_name,
        )

    @staticmethod
    def get_schema_pydantic_base_model(
        schema_pydantic_base_model_name: Literal[
            'all', 'only-expectation', 'only-choice',
        ],
    ) -> type[BaseModel]:
        return StructuredOutputFormatFactory.create_structured_output_format(
            schema_pydantic_base_model_name=schema_pydantic_base_model_name,
        )

    @staticmethod
    def get_message_prompt_templates(
        agent_configs: list[AgentConfig],
    ) -> dict[str, HumanMessagePromptTemplate]:
        message_prompt_templates = {}
        participant_prompt_template_factory = ParticipantPromptTemplateFactory()
        for agent_config in agent_configs:
            message_prompt_template = participant_prompt_template_factory.get_message_prompt_template(
                message_prompt_template_name=agent_config.message_prompt_template_name,
            )
            message_prompt_templates[agent_config.agent_id] = message_prompt_template
        logger.trace(f"Message Prompt Templates: \n{message_prompt_templates}")
        return message_prompt_templates

