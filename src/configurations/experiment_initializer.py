from __future__ import annotations
from loguru import logger

import shutil
from pathlib import Path

from typing import TYPE_CHECKING, Literal
# if TYPE_CHECKING:


class ExperimentInitializer:
    @staticmethod
    def prepare_experiment_dir_with_index(
        experiment_base_dir: str | Path,
        experiment_times: int,
    ) -> Path:
        experiment_base_dir = Path(experiment_base_dir)
        for experiment_index in range(experiment_times):
            experiment_runtime_dir = experiment_base_dir / f'{experiment_index}'
            if not experiment_runtime_dir.exists():
                experiment_runtime_dir.mkdir()
                logger.debug(f"Created new experiment runtime directory: {experiment_runtime_dir}")
            ExperimentInitializer.copy_experiment_runtime_files(
                experiment_base_dir=experiment_base_dir,
                experiment_runtime_dir=experiment_runtime_dir,
            )
            logger.success(f"Copied configuration files to experiment runtime directory: {experiment_runtime_dir}")
        return experiment_base_dir

    @staticmethod
    def create_new_experiment_base_dir(
        experiment_base_dir: str | Path,
    ) -> Path:
        experiment_base_dir = Path(experiment_base_dir)
        experiment_runtime_dir = ExperimentInitializer.create_empty_experiment_dir(
            experiment_base_dir=experiment_base_dir,
        )
        ExperimentInitializer.copy_experiment_runtime_files(
            experiment_base_dir=experiment_base_dir,
            experiment_runtime_dir=experiment_runtime_dir,
        )
        logger.info(f"Created new experiment runtime directory: {experiment_runtime_dir}")
        return experiment_runtime_dir

    @staticmethod
    def create_empty_experiment_dir(
        experiment_base_dir: Path,
    ) -> Path:
        for experiment_index in range(1000):
            experiment_dir = experiment_base_dir / f'{experiment_index}'
            if not experiment_dir.exists():
                experiment_dir.mkdir()
        return experiment_base_dir

    @staticmethod
    def copy_experiment_runtime_files(
        experiment_base_dir: Path,
        experiment_runtime_dir: Path,
    ) -> None:
        environment_config_path = experiment_base_dir / 'environment_config.json'
        agent_configs_path = experiment_base_dir / 'agent_configs.jsonl'
        shutil.copy(
            src=environment_config_path,
            dst=experiment_runtime_dir / 'environment_config.json',
        )
        logger.debug(f"Copied environment_config.json to: {environment_config_path}")
        shutil.copy(
            src=agent_configs_path,
            dst=experiment_runtime_dir / 'agent_configs.jsonl',
        )
        logger.debug(f"Copied agent_configs.jsonl to: {agent_configs_path}")

