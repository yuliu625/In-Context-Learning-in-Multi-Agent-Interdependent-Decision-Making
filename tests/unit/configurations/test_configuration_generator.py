from __future__ import annotations
import pytest
from loguru import logger

from src.configurations.configuration_generator import ConfigurationGenerator

from tests.data.configuration_persistence_cases import (
    EXPERIMENT_CONFIGURATION_DICT_CASES,
    EXPERIMENT_PATH_DICT_CASES,
)

from pathlib import Path

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestConfigurationGenerator:
    @pytest.mark.parametrize(
        'experiment_control_template_file_path', ["./configs/experiment_control_template.yaml"]
    )
    @pytest.mark.parametrize(
        'persistence_config_kwargs', EXPERIMENT_PATH_DICT_CASES,
    )
    @pytest.mark.parametrize(
        'runtime_configuration_kwargs', EXPERIMENT_CONFIGURATION_DICT_CASES,
    )
    def test_render_and_save_experiment_control_template(
        self,
        experiment_control_template_file_path: str | Path,
        persistence_config_kwargs: dict,
        runtime_configuration_kwargs: dict,
        tmp_path: Path,
    ):
        ConfigurationGenerator.render_and_save_experiment_control_template(
            experiment_control_template_file_path=experiment_control_template_file_path,
            config_kwargs=dict(
                experiment_root_dir=tmp_path,
                experiment_name='test_experiment_name',
                experiment_times=3,
                **runtime_configuration_kwargs,
            ),
            experiment_control_file_path=tmp_path / 'experiment_control.yaml',
        )

