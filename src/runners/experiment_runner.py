from __future__ import annotations
from loguru import logger

from src.runners.fsm_runner import FSMRunner

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from pathlib import Path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.mas_state import MASState
    from langgraph.checkpoint.base import BaseCheckpointSaver


class ExperimentRunner:
    @staticmethod
    async def search_and_run_unfinished_experiments(
        experiment_base_dir: str | Path,
        experiment_index_search_range: int = 10000,
    ) -> None:
        experiment_base_dir = Path(experiment_base_dir)
        for experiment_index in range(experiment_index_search_range):
            experiment_runtime_dir = experiment_base_dir / f'{experiment_index}'
            if not experiment_runtime_dir.exists():
                logger.success(f"Finished all experiments. Experiment index: {experiment_index}")
                return
            else:
                if not ExperimentRunner.check_is_finished_experiment(experiment_runtime_dir=experiment_runtime_dir, ):
                    logger.info(f"Find unfinished experiment. Experiment index: {experiment_index}")
                    await ExperimentRunner.a_run_experiment_with_sqlite_checkpointer(
                        experiment_runtime_dir=experiment_runtime_dir,
                    )

    @staticmethod
    async def a_run_experiment_with_sqlite_checkpointer(
        experiment_runtime_dir: str | Path,
    ) -> MASState:
        experiment_runtime_dir = Path(experiment_runtime_dir)
        async with AsyncSqliteSaver.from_conn_string(str(experiment_runtime_dir / 'checkpoints.db')) as checkpointer:
            result_state = await ExperimentRunner.a_run_experiment(
                experiment_runtime_dir=experiment_runtime_dir,
                checkpointer=checkpointer,
            )
            return result_state

    @staticmethod
    async def a_run_experiment(
        experiment_runtime_dir: str | Path,
        checkpointer: BaseCheckpointSaver | None = None,
    ) -> MASState:
        logger.info(f"Initializing a fsm_runner.")
        fsm_runner = FSMRunner(
            dir_to_load_and_save=experiment_runtime_dir,
            checkpointer=checkpointer,
        )
        runnable_config = ExperimentRunner.get_runnable_config(
            thread_id='0',
        )
        result_state = await fsm_runner.a_run_graph(
            config=runnable_config,
        )
        logger.success(f"Finished an experiment. Experiment Directory: {experiment_runtime_dir}")
        return result_state

    @staticmethod
    def get_runnable_config(
        thread_id: str,
    ) -> dict:
        runnable_config = dict(
            configurable=dict(thread_id=thread_id),
        )
        logger.trace(f"runnable_config: {runnable_config}")
        return runnable_config

    @staticmethod
    def check_is_finished_experiment(
        experiment_runtime_dir: Path,
    ) -> bool:
        path_to_results = experiment_runtime_dir / 'results.jsonl'
        return path_to_results.exists()

