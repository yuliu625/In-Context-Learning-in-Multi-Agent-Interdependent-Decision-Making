from __future__ import annotations
import pytest
from loguru import logger

from src.schemas.mas_state import MASState
from src.fsm.nodes.node_building_tools import NodeBuildingTools
from src.fsm.nodes.mas_initializer import MASInitializer

from tests.data.experiment_config_cases import (
    ENVIRONMENT_CONFIG_CASES,
    AGENT_CONFIG_CASES,
    AGENT_CONFIGS_CASES,
)

from langchain_core.messages import (
    HumanMessage,
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.experiment_configs import (
        EnvironmentConfig,
        AgentConfig,
    )


class TestMASInitializer:
    @pytest.mark.parametrize(
        'environment_config', ENVIRONMENT_CONFIG_CASES,
    )
    @pytest.mark.parametrize(
        'agent_configs', AGENT_CONFIGS_CASES,
    )
    @pytest.mark.parametrize(
        'experiment_round', [0,],
    )
    def test_process_state(
        self,
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
        experiment_round: int,
    ):
        message_prompt_templates = NodeBuildingTools.get_message_prompt_templates(
            agent_configs=agent_configs,
        )
        mas_initializer = MASInitializer(
            message_prompt_templates=message_prompt_templates,
        )
        mas_state = MASState(
            environment_config=environment_config,
            agent_configs=agent_configs,
            experiment_round=experiment_round,
        )
        state = mas_initializer.process_state(
            state=mas_state,
            config=None,
        )
        logger.debug(f"MAS State: {state}")

    @pytest.mark.parametrize(
        'environment_config', ENVIRONMENT_CONFIG_CASES,
    )
    @pytest.mark.parametrize(
        'agent_configs', AGENT_CONFIGS_CASES,
    )
    @pytest.mark.parametrize(
        'experiment_round', [0,],
    )
    def test_initialize_environment_message(
        self,
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
        experiment_round: int,
    ):
        message_prompt_templates = NodeBuildingTools.get_message_prompt_templates(
            agent_configs=agent_configs,
        )
        environment_messages = MASInitializer.initialize_environment_message(
            message_prompt_templates=message_prompt_templates,
            environment_config=environment_config,
            agent_configs=agent_configs,
            experiment_round=experiment_round,
        )
        logger.debug(f"environment_messages: {environment_messages}")
        assert all(
            len(value) == 1
            for _, value in environment_messages.items()
        )
        assert all(
            isinstance(key, str) and isinstance(value[0], HumanMessage)
            for key, value in environment_messages.items()
        )

