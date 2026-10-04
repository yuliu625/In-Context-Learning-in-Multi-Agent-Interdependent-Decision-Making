from __future__ import annotations
import pytest
from loguru import logger

from src.io.state_io import StateIO

from tests.data.experiment_directory_cases import (
    EXPERIMENT_DIRECTORY_CASES,
    RESULT_DIRECTORY_CASES,
)

from pathlib import Path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.experiment_configs import StateAndMASConfigs


class TestStateIO:
    @pytest.mark.parametrize(
        'experiment_index_dir', EXPERIMENT_DIRECTORY_CASES,
    )
    def test_load_environment_config(
        self,
        data_dir: Path,
        experiment_index_dir: str | Path,
    ):
        dir_to_load_and_save = data_dir / experiment_index_dir
        environment_config_path = dir_to_load_and_save / 'environment_config.json'
        environment_config = StateIO.load_environment_config(
            environment_config_path=environment_config_path,
        )

    @pytest.mark.parametrize(
        'experiment_index_dir', EXPERIMENT_DIRECTORY_CASES,
    )
    def test_load_agent_configs(
        self,
        data_dir: Path,
        experiment_index_dir: str | Path,
    ):
        dir_to_load_and_save = data_dir / experiment_index_dir
        agent_configs_path = dir_to_load_and_save / 'agent_configs.jsonl'
        agent_configs = StateIO.load_agent_configs(
            agent_configs_path=agent_configs_path,
        )

    @pytest.mark.parametrize(
        'experiment_index_dir', RESULT_DIRECTORY_CASES,
    )
    def test_load_chat_histories(
        self,
        data_dir: Path,
        experiment_index_dir: str | Path,
    ):
        dir_to_load_and_save = data_dir / experiment_index_dir
        chat_histories_path = dir_to_load_and_save / 'chat_histories.jsonl'
        chat_histories = StateIO.load_chat_histories(
            chat_histories_path=chat_histories_path,
        )

    @pytest.mark.parametrize(
        'experiment_index_dir', RESULT_DIRECTORY_CASES,
    )
    def test_load_results(
        self,
        data_dir: Path,
        experiment_index_dir: str | Path,
    ):
        dir_to_load_and_save = data_dir / experiment_index_dir
        results_path = dir_to_load_and_save / 'results.jsonl'
        results = StateIO.load_results(
            results_path=results_path,
        )

    @pytest.mark.parametrize(
        'experiment_index_dir', RESULT_DIRECTORY_CASES,
    )
    def test_load_state_and_mas_configs(
        self,
        data_dir: Path,
        experiment_index_dir: str | Path,
    ):
        dir_to_load_and_save = data_dir / experiment_index_dir
        state_and_mas_configs = StateIO.load_state_and_mas_configs(
            dir_to_load_and_save=dir_to_load_and_save
        )

