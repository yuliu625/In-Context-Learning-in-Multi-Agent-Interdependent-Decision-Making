from __future__ import annotations
import asyncio
import pytest
from loguru import logger

from src.runners.fsm_runner import FSMRunner

from tests.data.experiment_directory_cases import (
    EXPERIMENT_DIRECTORY_CASES,
)

from pathlib import Path
import shutil

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig
    from langgraph.checkpoint.base import BaseCheckpointSaver


class TestFSMRunner:
    @pytest.mark.parametrize(
        "experiment_runtime_dir", EXPERIMENT_DIRECTORY_CASES,
    )
    async def test_a_run_graph(
        self,
        data_dir: Path,
        experiment_runtime_dir: str | Path,
        tmp_path: Path,
    ):
        shutil.copytree(
            src=data_dir / experiment_runtime_dir,
            dst=tmp_path,
            dirs_exist_ok=True,
        )
        fsm_runner = FSMRunner(
            dir_to_load_and_save=tmp_path,
            checkpointer=None,
        )
        result_state = await fsm_runner.a_run_graph(
            config=None,
        )
        logger.debug(f"result_state: {result_state}")
        assert (tmp_path / "chat_histories.jsonl").exists()
        assert (tmp_path / "results.jsonl").exists()

