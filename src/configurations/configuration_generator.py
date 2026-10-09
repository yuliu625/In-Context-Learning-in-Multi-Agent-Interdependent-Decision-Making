from __future__ import annotations
from loguru import logger

from jinja2 import Template
from pathlib import Path

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class ConfigurationGenerator:
    @staticmethod
    def batch_make_configuration_files(
        template_path: str | Path,
        configs_kwargs: dict,
        configuration_paths: list[str | Path],
    ) -> None:
        raise NotImplementedError

    @staticmethod
    def make_experiment_control_file(
        experiment_control_template_file_path: str | Path,
        persistence_config_kwargs: dict,
        runtime_config_kwargs: dict,
        experiment_control_file_path: str | Path,
    ) -> str:
        configuration = ConfigurationGenerator.render_and_save_experiment_control_template(
            experiment_control_template_file_path=experiment_control_template_file_path,
            config_kwargs=dict(
                **persistence_config_kwargs,
                **runtime_config_kwargs,
            ),
            experiment_control_file_path=experiment_control_file_path,
        )
        logger.trace(f"Saved Experiment Control File at: {experiment_control_file_path}")
        return configuration

    @staticmethod
    def render_and_save_experiment_control_template(
        experiment_control_template_file_path: str | Path,
        config_kwargs: dict,
        experiment_control_file_path: str | Path,
    ) -> str:
        logger.debug(f"Loading Template File from: {experiment_control_template_file_path}")
        with open(experiment_control_template_file_path, 'r', encoding='utf-8', ) as template:
            template = Template(template.read())
        logger.trace(f"template: {template}")
        logger.debug(f"config_kwargs: {config_kwargs}")
        configuration = template.render(**config_kwargs)
        logger.trace(f"configuration: {configuration}")
        with open(experiment_control_file_path, 'w', encoding='utf-8', ) as file:
            file.write(configuration)
        logger.success(f"Saved Experiment Control File at: {experiment_control_file_path}")
        return configuration

