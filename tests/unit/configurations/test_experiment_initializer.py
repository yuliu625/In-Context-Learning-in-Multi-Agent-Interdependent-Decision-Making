from __future__ import annotations
import pytest
from loguru import logger

from src.configurations.experiment_initializer import (
    ExperimentInitializer,
)

from tests.data.experiment_directory_cases import (
    EXPERIMENT_DIRECTORY_CASES,
)

from pathlib import Path
import shutil

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestExperimentInitializer:
    @pytest.mark.parametrize(
        'experiment_base_dir', EXPERIMENT_DIRECTORY_CASES,
    )
    @pytest.mark.parametrize(
        'experiment_times', [3, 5,],
    )
    def test_prepare_experiment_dir_with_index(
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

