from __future__ import annotations
import pytest
from loguru import logger

from src.io.state_builder import StateBuilder

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
        ExperimentResult,
    )
    from langchain_core.messages import AnyMessage


class TestStateBuilder:
    @pytest.mark.parametrize(
        'environment_config', ENVIRONMENT_CONFIG_CASES,
    )
    @pytest.mark.parametrize(
        'agent_configs', AGENT_CONFIGS_CASES,
    )
    @pytest.mark.parametrize(
        'chat_histories', [None,],
    )
    @pytest.mark.parametrize(
        'results', [None,],
    )
    def test_build_mas_state(
        self,
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
        chat_histories: dict[str, list[AnyMessage]] | None,
        results: list[ExperimentResult] | None,
    ):
        mas_state = StateBuilder.build_mas_state(
            environment_config=environment_config,
            agent_configs=agent_configs,
            chat_histories=chat_histories,
            results=results,
        )

