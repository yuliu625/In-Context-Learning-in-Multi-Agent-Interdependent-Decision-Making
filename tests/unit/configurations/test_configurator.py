from __future__ import annotations
import pytest
from loguru import logger

from src.configurations.configurator import Configurator

from tests.data.configuration_persistence_cases import (
    EXPERIMENT_CONFIGURATION_DICT_CASES,
)

from pathlib import Path

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestConfigurator:
    @pytest.mark.parametrize(
        'experiment_configuration', EXPERIMENT_CONFIGURATION_DICT_CASES,
    )
    def test_make_default_configuration_files(
        self,
        tmp_path: Path,
        experiment_configuration: dict,
    ):
        Configurator.make_default_configuration_files(
            dir_to_load_and_save=tmp_path,
            **experiment_configuration,
        )
        assert (tmp_path / 'environment_config.json').exists()
        assert (tmp_path / 'agent_configs.jsonl').exists()

