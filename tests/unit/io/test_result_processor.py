from __future__ import annotations
import pytest
from loguru import logger

from src.io.result_processor import (
    ResultProcessor,
)

from tests.data.experiment_directory_cases import (
    RESULT_DIRECTORY_CASES,
)

from pathlib import Path
import shutil

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestResultProcessor:
    @pytest.mark.parametrize(
        'experiment_runtime_dir', RESULT_DIRECTORY_CASES,
    )
    def test_merge_results_and_chat_histories(
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
        assert (tmp_path / "environment_config.json").exists()
        assert (tmp_path / "agent_configs.jsonl").exists()
        assert (tmp_path / "chat_histories.jsonl").exists()
        assert (tmp_path / "results.jsonl").exists()
        ResultProcessor.merge_results_and_chat_histories(
            dir_to_load_and_save=tmp_path,
        )
        assert (tmp_path / "all_in_one.jsonl").exists()

