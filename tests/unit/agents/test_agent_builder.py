from __future__ import annotations
import asyncio
import pytest
from loguru import logger

from src.schemas.experiment_configs import (
    EnvironmentConfig,
    AgentConfig,
)
from src.schemas.interaction_protocols import AgentResponse
from src.agents.builders.agent_builder import AgentBuilder

from tests.data.experiment_config_cases import (
    ENVIRONMENT_CONFIG_CASES,
    AGENT_CONFIG_CASES,
    AGENT_CONFIGS_CASES,
)
from tests.data.human_message_cases import (
    EXPERIMENT_HUMAN_MESSAGE_CONTENT_CASES,
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)
from langchain_core.prompts import ChatPromptTemplate

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestAgentBuilder:
    @pytest.mark.parametrize(
        'environment_config', ENVIRONMENT_CONFIG_CASES,
    )
    @pytest.mark.parametrize(
        'agent_config', AGENT_CONFIG_CASES,
    )
    @pytest.mark.parametrize(
        'human_message_content', EXPERIMENT_HUMAN_MESSAGE_CONTENT_CASES,
    )
    async def test_set_agent_system_message_prompt_template(
        self,
        environment_config: EnvironmentConfig,
        agent_config: AgentConfig,
        human_message_content: str,
    ):
        agent = AgentBuilder.build_agent(
            environment_config=environment_config,
            agent_config=agent_config,
            model_configs=dict(),
        )
        agent = AgentBuilder.set_agent_system_message_prompt_template(
            agent=agent,
            environment_config=environment_config,
            agent_config=agent_config,
            network_size=6,
            standalone_values=[1, 2, 3, 4, 5, 6],
        )
        logger.info(f"chat_prompt_template: {agent._chat_prompt_template}")
        assert isinstance(agent._chat_prompt_template, ChatPromptTemplate)

    @pytest.mark.parametrize(
        'environment_config', ENVIRONMENT_CONFIG_CASES,
    )
    @pytest.mark.parametrize(
        'agent_config', AGENT_CONFIG_CASES,
    )
    @pytest.mark.parametrize(
        'human_message_content', EXPERIMENT_HUMAN_MESSAGE_CONTENT_CASES,
    )
    async def test_build_agent(
        self,
        environment_config: EnvironmentConfig,
        agent_config: AgentConfig,
        human_message_content: str,
    ):
        agent = AgentBuilder.build_agent(
            environment_config=environment_config,
            agent_config=agent_config,
            model_configs=dict(),
        )
        agent = AgentBuilder.set_agent_system_message_prompt_template(
            agent=agent,
            environment_config=environment_config,
            agent_config=agent_config,
            network_size=6,
            standalone_values=[1, 2, 3, 4, 5, 6],
        )
        response = await agent.a_get_agent_response(
            chat_history=[
                HumanMessage(
                    content=human_message_content,
                ),
            ],
        )
        logger.info(f"response: {response}")
        assert isinstance(response, AgentResponse)

    @pytest.mark.parametrize(
        'environment_config', ENVIRONMENT_CONFIG_CASES,
    )
    @pytest.mark.parametrize(
        'agent_configs', AGENT_CONFIGS_CASES,
    )
    @pytest.mark.parametrize(
        'human_message_content', EXPERIMENT_HUMAN_MESSAGE_CONTENT_CASES,
    )
    async def test_build_agents(
        self,
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
        human_message_content: str,
    ):
        agents = AgentBuilder.batch_build_agents(
            environment_config=environment_config,
            agent_configs=agent_configs,
        )
        response = await agents[agent_configs[0].agent_id].a_get_agent_response(
            chat_history=[
                HumanMessage(
                    content=human_message_content,
                ),
            ],
        )
        logger.info(f"response: {response}")
        assert isinstance(response, AgentResponse)

