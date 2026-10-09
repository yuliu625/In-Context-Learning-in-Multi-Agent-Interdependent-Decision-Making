from __future__ import annotations
from loguru import logger

from src.schemas.experiment_configs import (
    EnvironmentConfig,
    AgentConfig,
)

from pathlib import Path

from typing import TYPE_CHECKING, Literal
# if TYPE_CHECKING:


class ConfigurationChecker:
    @staticmethod
    def check_schemas(
        environment_config_dict: dict,
        agent_configs_list: list[dict],
    ) -> bool:
        environment_config = EnvironmentConfig.model_validate(
            environment_config_dict,
        )
        agent_configs = [
            AgentConfig.model_validate(agent_config_dict)
            for agent_config_dict in agent_configs_list
        ]
        return True

    @staticmethod
    def check_agent_ids(
        agent_configs: list[AgentConfig],
    ) -> bool:
        agent_ids = set(agent_config.agent_id for agent_config in agent_configs)
        assert len(agent_ids) == len(agent_configs)
        return len(agent_ids) == len(agent_configs)

    @staticmethod
    def check_model_name(
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
        model_name: str,
    ) -> bool:
        raise NotImplementedError

