from __future__ import annotations
from loguru import logger

from src.io.state_io import StateIO
from src.io.state_builder import StateBuilder
from src.fsm.graphs.graph_factory import GraphFactory

from pathlib import Path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.mas_state import MASState
    from src.schemas.experiment_configs import StateAndMASConfigs
    from langchain_core.runnables import RunnableConfig
    from langgraph.graph.state import CompiledStateGraph
    from langgraph.checkpoint.base import BaseCheckpointSaver


class FSMRunner:
    def __init__(
        self,
        dir_to_load_and_save: str | Path,
        checkpointer: BaseCheckpointSaver | None = None,
    ):
        self.dir_to_load_and_save = dir_to_load_and_save
        self.state_and_mas_configs = StateIO.load_state_and_mas_configs(
            dir_to_load_and_save=dir_to_load_and_save,
        )
        self.mas_state = self._initialize_state(
            state_and_mas_configs=self.state_and_mas_configs,
        )
        self.graph = self._initialize_graph(
            state_and_mas_configs=self.state_and_mas_configs,
            checkpointer=checkpointer,
        )

    async def a_run_graph(
        self,
        config: RunnableConfig | None = None,
    ) -> MASState:
        logger.info(f"FSM Start.")
        result_state = await self.graph.ainvoke(
            input=self.mas_state,
            config=config,
        )
        logger.info(f"FSM Finish.")
        logger.debug(f"Result State: {result_state}")
        self._save_state(
            mas_state=result_state,
            dir_to_load_and_save=self.dir_to_load_and_save,
        )
        return result_state

    def _initialize_state(
        self,
        state_and_mas_configs: StateAndMASConfigs,
    ) -> MASState:
        mas_state = StateBuilder.build_mas_state(
            environment_config=state_and_mas_configs.environment_config,
            agent_configs=state_and_mas_configs.agent_configs,
            chat_histories=state_and_mas_configs.chat_histories,
            results=state_and_mas_configs.results,
        )
        logger.debug(f"Initial State: {mas_state}")
        return mas_state

    def _initialize_graph(
        self,
        state_and_mas_configs: StateAndMASConfigs,
        checkpointer: BaseCheckpointSaver | None = None,
    ) -> CompiledStateGraph:
        graph = GraphFactory.create_default_graph(
            environment_config=state_and_mas_configs.environment_config,
            agent_configs=state_and_mas_configs.agent_configs,
            checkpointer=checkpointer,
        )
        logger.debug(f"Initial Graph: {graph}")
        return graph

    def _save_state(
        self,
        mas_state: MASState | dict,
        dir_to_load_and_save: str | Path,
    ) -> None:
        StateIO.save_state(
            state=mas_state,
            dir_to_save_result=dir_to_load_and_save,
        )
        logger.success(f"Saved MAS State in: {dir_to_load_and_save}")

