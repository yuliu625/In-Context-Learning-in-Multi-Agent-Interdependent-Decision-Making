from __future__ import annotations
import pytest
from loguru import logger

from src.fsm.nodes.node_building_tools import NodeBuildingTools

from tests.data.experiment_config_cases import (
    AGENT_CONFIGS_CASES,
)

from langchain_core.prompts import HumanMessagePromptTemplate

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.experiment_configs import AgentConfig


class TestNodeBuildingTools:
    @pytest.mark.parametrize(
        'agent_configs', AGENT_CONFIGS_CASES,
    )
    def test_get_message_prompt_templates(
        self,
        agent_configs: list[AgentConfig],
    ):
        messages_prompt_templates = NodeBuildingTools.get_message_prompt_templates(
            agent_configs=agent_configs,
        )
        logger.debug(f"messages_prompt_templates: {messages_prompt_templates}")
        assert isinstance(messages_prompt_templates, dict)
        assert all(
            isinstance(key, str) and isinstance(value, HumanMessagePromptTemplate)
            for key, value in messages_prompt_templates.items()
        )

