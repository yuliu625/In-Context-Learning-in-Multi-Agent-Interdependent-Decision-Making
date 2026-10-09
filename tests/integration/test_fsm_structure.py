from __future__ import annotations
import pytest
from loguru import logger

from src.utils.graph_visualizer import GraphVisualizer
from src.fsm.graphs.graph_factory import GraphFactory

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
    from langgraph.checkpoint.base import BaseCheckpointSaver


class TestFSMStructure:
    @pytest.mark.parametrize(
        'environment_config', ENVIRONMENT_CONFIG_CASES,
    )
    @pytest.mark.parametrize(
        'agent_configs', AGENT_CONFIGS_CASES,
    )
    def test_fsm_structure(
        self,
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
    ):
        graph = GraphFactory.create_default_graph(
            environment_config=environment_config,
            agent_configs=agent_configs,
            checkpointer=None,
        )
        mermai_code = GraphVisualizer.get_mermaid_code(
            graph=graph,
        )
        logger.debug(f"Mermaid Code: \n{mermai_code}")

