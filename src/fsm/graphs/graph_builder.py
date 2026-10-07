from __future__ import annotations
from loguru import logger

from src.schemas.mas_state import MASState
from src.fsm.nodes.mas_initializer import MASInitializer
from src.fsm.nodes.message_handler import MessageHandler
from src.fsm.nodes.llm_caller import LLMCaller
from src.fsm.nodes.result_collector import ResultCollector
from src.fsm.edges.is_experiment_continue import is_experiment_continue
from src.fsm.edges.is_experiment_finished import is_experiment_finished

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from langgraph.graph.state import CompiledStateGraph
    from langgraph.checkpoint.base import BaseCheckpointSaver


class GraphBuilder:
    def __init__(
        self,
        mas_initializer: MASInitializer,
        message_handler: MessageHandler,
        llm_caller: LLMCaller,
        result_collector: ResultCollector,
    ):
        self.graph_builder = StateGraph(MASState)
        self.mas_initializer = mas_initializer
        self.message_handler = message_handler
        self.llm_caller = llm_caller
        self.result_collector = result_collector

    def build_graph(
        self,
        checkpointer: BaseCheckpointSaver | None = None,
    ) -> CompiledStateGraph:
        self._add_nodes()
        logger.debug(f"Registered Nodes.")
        self._add_edges()
        logger.debug(f"Registered Edges.")
        graph = self.graph_builder.compile(
            checkpointer=checkpointer,
        )
        logger.debug(f"Compiled Graph: {graph}")
        return graph

    def _add_nodes(
        self,
    ):
        self.graph_builder.add_node('mas_initializer', self.mas_initializer.process_state,)
        self.graph_builder.add_node('message_handler', self.message_handler.process_state,)
        self.graph_builder.add_node('llm_caller', self.llm_caller.process_state,)
        self.graph_builder.add_node('result_collector', self.result_collector.process_state,)

    def _add_edges(
        self,
    ):
        self.graph_builder.add_edge(START, 'mas_initializer',)
        self.graph_builder.add_conditional_edges(
            'mas_initializer',
            is_experiment_finished,
            {
                True: END,
                False: 'llm_caller',
            },
        )
        self.graph_builder.add_edge('message_handler', 'llm_caller',)
        self.graph_builder.add_edge('llm_caller', 'result_collector',)
        self.graph_builder.add_conditional_edges(
            'result_collector',
            is_experiment_continue,
            {
                True: 'message_handler',
                False: END,
            },
        )

