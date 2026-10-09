from __future__ import annotations
import asyncio
import pytest
from loguru import logger

from src.runners.experiment_runner import (
    ExperimentRunner,
)
from src.configurations.experiment_initializer import (
    ExperimentInitializer,
)

from tests.data.experiment_directory_cases import (
    EXPERIMENT_DIRECTORY_CASES,
)

from pathlib import Path
import shutil

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig
    from langgraph.checkpoint.base import BaseCheckpointSaver


class TestExperimentRunner:
    @pytest.mark.parametrize(
        "experiment_base_dir", EXPERIMENT_DIRECTORY_CASES,
    )
    @pytest.mark.parametrize(
        'experiment_times', [2,],
    )
    async def test_search_and_run_unfinished_experiments(
        self,
        data_dir: Path,
        experiment_base_dir: str | Path,
        experiment_times: int,
        tmp_path: Path,
    ):
        shutil.copytree(
            data_dir / experiment_base_dir,
            tmp_path,
            dirs_exist_ok=True,
        )
        assert (tmp_path / "environment_config.json").exists()
        assert (tmp_path / "agent_configs.jsonl").exists()
        ExperimentInitializer.prepare_experiment_dir_with_index(
            experiment_base_dir=tmp_path,
            experiment_times=experiment_times,
        )
        for experiment_index in range(experiment_times):
            experiment_runtime_dir = tmp_path / f"{experiment_index}"
            assert experiment_runtime_dir.exists()
            assert (experiment_runtime_dir / "environment_config.json").exists()
            assert (experiment_runtime_dir / "agent_configs.jsonl").exists()
        await ExperimentRunner.search_and_run_unfinished_experiments(
            experiment_base_dir=tmp_path,
            experiment_index_search_range=10000,
        )
        for experiment_index in range(experiment_times):
            experiment_runtime_dir = tmp_path / f"{experiment_index}"
            assert (experiment_runtime_dir / "chat_histories.jsonl").exists()
            assert (experiment_runtime_dir / "results.jsonl").exists()

