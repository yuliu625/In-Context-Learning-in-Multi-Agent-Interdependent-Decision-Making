from __future__ import annotations
from loguru import logger
from pydantic import BaseModel, Field, ConfigDict

from src.schemas.calculation_fields import ExperimentResult

from langchain_core.messages import AnyMessage
# import pandas as pd

from typing import TYPE_CHECKING, Literal
# if TYPE_CHECKING:


class EnvironmentConfig(BaseModel):
    network_effect: float
    prices: list[float]
    utility_function_name: Literal[
        'linear',
    ]
    schema_pydantic_base_model_name: Literal[
        'all', 'only-expectation', 'only-choice',
    ]
    chat_history_length: int


class AgentConfig(BaseModel):
    agent_id: str
    model_client: Literal[
        'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
    ]
    model_name: str
    is_reasoning: bool
    model_configs: dict
    standalone_value: float
    system_message_prompt_template_name: str
    message_prompt_template_name: str


class LLMConfigs(BaseModel):
    temperature: float
    top_p: float


class StateAndMASConfigs(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    environment_config: EnvironmentConfig
    agent_configs: list[AgentConfig]
    chat_histories: dict[str, list[AnyMessage]] | None
    results: list[ExperimentResult] | None

