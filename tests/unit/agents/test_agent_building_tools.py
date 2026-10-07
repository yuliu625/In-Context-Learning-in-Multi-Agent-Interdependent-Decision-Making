from __future__ import annotations
import pytest
from loguru import logger

from src.schemas.experiment_configs import (
    EnvironmentConfig,
    AgentConfig,
)
from src.agents.builders.agent_building_tools import AgentBuildingTools

from tests.data.experiment_config_cases import (
    ENVIRONMENT_CONFIG_CASES,
    AGENT_CONFIG_CASES,
    AGENT_CONFIGS_CASES,
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestAgentBuildingTools:
    @pytest.mark.parametrize(
        'agent_config', AGENT_CONFIG_CASES,
    )
    def test_get_chat_prompt_template(
        self,
        agent_config: AgentConfig,
    ):
        chat_prompt_template = AgentBuildingTools.get_chat_prompt_template(
            agent_config=agent_config,
        )
        logger.info(f'chat_prompt_template: {chat_prompt_template}')
        assert isinstance(chat_prompt_template, ChatPromptTemplate)

    @pytest.mark.parametrize(
        'agent_config', AGENT_CONFIG_CASES,
    )
    def test_get_llm(
        self,
        agent_config: AgentConfig,
    ):
        llm = AgentBuildingTools.get_llm(
            agent_config=agent_config,
            model_configs=dict(),
        )
        response = llm.invoke("What is your model id?")
        logger.info(f'response: {response}')
        assert isinstance(llm, BaseChatModel)

    @pytest.mark.parametrize(
        'environment_config', ENVIRONMENT_CONFIG_CASES,
    )
    def test_get_schema_pydantic_base_model(
        self,
        environment_config: EnvironmentConfig,
    ):
        schema_pydantic_base_model = AgentBuildingTools.get_schema_pydantic_base_model(
            environment_config=environment_config,
        )
        logger.info(f'schema_pydantic_base_model: {schema_pydantic_base_model}')
        assert isinstance(schema_pydantic_base_model, type(BaseModel))

    @pytest.mark.parametrize(
        'agent_configs', AGENT_CONFIGS_CASES,
    )
    def test_get_mapping_from_agents_to_rate_limiter(
        self,
        agent_configs: list[AgentConfig],
    ):
        rate_limiter_mapping = AgentBuildingTools.get_mapping_from_agents_to_rate_limiter(
            agent_configs=agent_configs,
        )
        logger.info(f'rate_limiter_mapping: {rate_limiter_mapping}')
        assert isinstance(rate_limiter_mapping, dict)

