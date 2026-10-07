from __future__ import annotations
from loguru import logger

from src.agents.builders.agent_builder import AgentBuilder
from src.fsm.nodes.mas_initializer import MASInitializer
from src.fsm.nodes.message_handler import MessageHandler
from src.fsm.nodes.llm_caller import LLMCaller
from src.fsm.nodes.result_collector import ResultCollector
from src.fsm.nodes.node_building_tools import NodeBuildingTools

from typing import TYPE_CHECKING, Literal, Callable
if TYPE_CHECKING:
    from src.schemas.experiment_configs import (
        EnvironmentConfig,
        AgentConfig,
    )


class NodeFactory:
    @staticmethod
    def create_mas_initializer(
        agent_configs: list[AgentConfig],
    ) -> MASInitializer:
        message_prompt_templates = NodeBuildingTools.get_message_prompt_templates(
            agent_configs=agent_configs,
        )
        mas_initializer = MASInitializer(
            message_prompt_templates=message_prompt_templates,
        )
        logger.debug(f"Created Mas Initializer.")
        return mas_initializer

    @staticmethod
    def create_message_handler(
        agent_configs: list[AgentConfig],
    ) -> MessageHandler:
        message_prompt_templates = NodeBuildingTools.get_message_prompt_templates(
            agent_configs=agent_configs,
        )
        message_handler = MessageHandler(
            message_prompt_templates=message_prompt_templates,
        )
        logger.debug(f"Created Message Handler.")
        return message_handler

    @staticmethod
    def create_llm_caller(
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
    ) -> LLMCaller:
        agents = AgentBuilder.batch_build_agents(
            environment_config=environment_config,
            agent_configs=agent_configs,
        )
        llm_caller = LLMCaller(
            agents=agents,
        )
        logger.debug(f"Created LLM Caller.")
        return llm_caller

    @staticmethod
    def create_result_collector(
        environment_config: EnvironmentConfig,
    ) -> ResultCollector:
        utility_function = NodeBuildingTools.get_utility_function(
            utility_function_name=environment_config.utility_function_name,
        )
        result_collector = ResultCollector(
            utility_function=utility_function,
        )
        logger.debug(f"Created Result Collector.")
        return result_collector

