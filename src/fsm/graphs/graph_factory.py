from __future__ import annotations
from loguru import logger

from src.fsm.nodes.node_factory import NodeFactory
from src.fsm.graphs.graph_builder import GraphBuilder

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.experiment_configs import (
        EnvironmentConfig,
        AgentConfig,
    )
    from langgraph.checkpoint.base import BaseCheckpointSaver


class GraphFactory:
    @staticmethod
    def create_default_graph(
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
        checkpointer: BaseCheckpointSaver | None = None,
    ):
        mas_initializer = NodeFactory.create_mas_initializer(
            agent_configs=agent_configs,
        )
        message_handler = NodeFactory.create_message_handler(
            agent_configs=agent_configs,
        )
        llm_caller = NodeFactory.create_llm_caller(
            environment_config=environment_config,
            agent_configs=agent_configs,
        )
        result_collector = NodeFactory.create_result_collector(
            environment_config=environment_config,
        )
        graph_builder = GraphBuilder(
            mas_initializer=mas_initializer,
            message_handler=message_handler,
            llm_caller=llm_caller,
            result_collector=result_collector,
        )
        graph = graph_builder.build_graph(
            checkpointer=checkpointer,
        )
        logger.info(f"Created Graph: {graph}")
        return graph

