from __future__ import annotations
from loguru import logger

from src.schemas.experiment_configs import (
    EnvironmentConfig,
    AgentConfig,
)

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


ENVIRONMENT_CONFIG_CASES = [
    EnvironmentConfig(
        network_effect=0.5,
        prices=[2.24, 2.99, 3.74, 4.49, 5.24, 5.99,],
        utility_function_name='linear',
        schema_pydantic_base_model_name='only-expectation',
        chat_history_length=13,
    ),
]


AGENT_CONFIG_CASES = [
    AgentConfig(
        agent_id='agent_0',
        model_client='ollama',
        model_name='qwen2.5:0.5b',
        is_reasoning=False,
        model_configs=dict(),
        standalone_value=5.0,
        system_message_prompt_template_name='demo',
        message_prompt_template_name='demo',
    ),
    AgentConfig(
        agent_id='agent_1',
        model_client='ollama',
        model_name='qwen2.5:0.5b',
        is_reasoning=False,
        model_configs=dict(),
        standalone_value=2.0,
        system_message_prompt_template_name='demo',
        message_prompt_template_name='demo',
    ),
]


AGENT_CONFIGS_CASES = [
    [
        AgentConfig(
            agent_id='agent_0',
            model_client='ollama',
            model_name='qwen2.5:0.5b',
            is_reasoning=False,
            model_configs=dict(),
            standalone_value=5.0,
            system_message_prompt_template_name='demo',
            message_prompt_template_name='demo',
        ),
        AgentConfig(
            agent_id='agent_1',
            model_client='ollama',
            model_name='qwen2.5:0.5b',
            is_reasoning=False,
            model_configs=dict(),
            standalone_value=2.0,
            system_message_prompt_template_name='demo',
            message_prompt_template_name='demo',
        ),
    ],
]

