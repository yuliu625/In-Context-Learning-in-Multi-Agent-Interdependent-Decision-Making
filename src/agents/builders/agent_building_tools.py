from __future__ import annotations
from loguru import logger

from src.prompts.prompt_template_factories import ParticipantPromptTemplateFactory
from src.models.llm_factory import BaseLLMFactory
from src.models.rate_limiter_factory import RateLimiterFactory
from src.schemas.structured_output_format import StructuredOutputFormatFactory

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.experiment_configs import EnvironmentConfig, AgentConfig
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.rate_limiters import BaseRateLimiter
    from pydantic import BaseModel


class AgentBuildingTools:
    @staticmethod
    def get_chat_prompt_template(
        agent_config: AgentConfig,
    ) -> ChatPromptTemplate:
        participant_prompt_template_factory = ParticipantPromptTemplateFactory()
        chat_prompt_template = participant_prompt_template_factory.get_chat_prompt_template(
            system_message_prompt_template_name=agent_config.system_message_prompt_template_name,
        )
        logger.trace(f"Get chat_prompt_template using agent_config: \n{agent_config}")
        return chat_prompt_template

    @staticmethod
    def get_llm(
        agent_config: AgentConfig,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        llm = BaseLLMFactory.create_llm(
            model_client=agent_config.model_client,
            model_name=agent_config.model_name,
            model_configs={**(model_configs or {})},
        )
        logger.trace(f"Get llm using agent_config: \n{agent_config}")
        logger.trace(f"Get llm using model_configs: \n{model_configs}")
        return llm

    @staticmethod
    def get_schema_pydantic_base_model(
        environment_config: EnvironmentConfig,
    ) -> type[BaseModel]:
        schema_pydantic_base_model = StructuredOutputFormatFactory.create_structured_output_format(
            schema_pydantic_base_model_name=environment_config.schema_pydantic_base_model_name,
        )
        logger.trace(f"Get schema_pydantic_base_model using environment_config: \n{environment_config}")
        return schema_pydantic_base_model

    @staticmethod
    def get_mapping_from_agents_to_rate_limiter(
        agent_configs: list[AgentConfig],
    ) -> dict[str, BaseRateLimiter]:
        model_client_model_name_mapping = {}
        for agent_config in agent_configs:
            model_client_model_name_mapping.setdefault(
                f"{agent_config.model_client}--{agent_config.model_name}",
                RateLimiterFactory.create_rate_limiter(
                    model_client=agent_config.model_client,
                    model_name=agent_config.model_name,
                )
            )
        logger.trace(f"Get model_client_model_name_mapping: \n{model_client_model_name_mapping}")
        rate_limiter_mapping = {}
        for agent_config in agent_configs:
            rate_limiter_mapping[f"{agent_config.agent_id}"] = model_client_model_name_mapping[
                f"{agent_config.model_client}--{agent_config.model_name}"
            ]
        logger.trace(f"Get rate_limiter_mapping: \n{rate_limiter_mapping}")
        return rate_limiter_mapping

