from __future__ import annotations
import pytest
from loguru import logger

from src.schemas.mas_state import MASState
from src.fsm.nodes.node_factory import NodeFactory

from tests.data.experiment_config_cases import (
    ENVIRONMENT_CONFIG_CASES,
    AGENT_CONFIG_CASES,
    AGENT_CONFIGS_CASES,
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.experiment_configs import (
        EnvironmentConfig,
        AgentConfig,
    )


class TestNodeFactory:
    @pytest.mark.parametrize(
        'agent_configs', AGENT_CONFIGS_CASES,
    )
    def test_create_mas_initializer(
        self,
        agent_configs: list[AgentConfig],
    ):
        mas_initializer = NodeFactory.create_mas_initializer(
            agent_configs=agent_configs,
        )

    @pytest.mark.parametrize(
        'agent_configs', AGENT_CONFIGS_CASES,
    )
    def test_create_message_handler(
        self,
        agent_configs: list[AgentConfig],
    ):
        message_handler = NodeFactory.create_message_handler(
            agent_configs=agent_configs,
        )

    @pytest.mark.parametrize(
        'environment_config', ENVIRONMENT_CONFIG_CASES,
    )
    @pytest.mark.parametrize(
        'agent_configs', AGENT_CONFIGS_CASES,
    )
    def test_create_llm_caller(
        self,
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
    ):
        llm_caller = NodeFactory.create_llm_caller(
            environment_config=environment_config,
            agent_configs=agent_configs,
        )

    @pytest.mark.parametrize(
        'environment_config', ENVIRONMENT_CONFIG_CASES,
    )
    def test_create_result_collector(
        self,
        environment_config: EnvironmentConfig,
    ):
        result_collector = NodeFactory.create_result_collector(
            environment_config=environment_config,
        )

