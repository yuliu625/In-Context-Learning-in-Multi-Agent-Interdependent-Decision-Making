from __future__ import annotations
import sys
from loguru import logger

from src.configurations.configurator import Configurator
from src.configurations.experiment_initializer import ExperimentInitializer

from pathlib import Path
from omegaconf import OmegaConf
from pydantic import BaseModel

from typing import TYPE_CHECKING, Literal
# if TYPE_CHECKING:


class PersistenceConfig(BaseModel):
    experiment_root_dir: str
    experiment_name: str
    experiment_base_dir: str
    experiment_times: int


class RuntimeConfig(BaseModel):
    network_effect: float
    prices: list[float]
    utility_function_name: Literal[
        'linear',
    ]
    schema_pydantic_base_model_name: Literal[
        'all', 'only-expectation', 'only-choice',
    ]
    chat_history_length: int

    network_size: int
    model_client: Literal[
        'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
    ]
    model_name: str
    is_reasoning: bool
    model_configs: dict
    system_message_prompt_template_name: str
    message_prompt_template_name: str


class ExperimentControl(BaseModel):
    generator: PersistenceConfig
    experiment: RuntimeConfig


def load_and_parse_experiment_control_file(
    experiment_control_file_path: str | Path,
) -> ExperimentControl:
    experiment_control = OmegaConf.load(
        experiment_control_file_path,
    )
    experiment_control = OmegaConf.to_container(
        experiment_control,
        resolve=True,
        throw_on_missing=True,
    )
    experiment_control = ExperimentControl.model_validate(
        experiment_control,
    )
    return experiment_control


def make_experiment_configuration_files(
    experiment_control: ExperimentControl,
):
    Configurator.make_default_configuration_files(
        dir_to_load_and_save=experiment_control.generator.experiment_base_dir,
        network_effect=experiment_control.experiment.network_effect,
        prices=experiment_control.experiment.prices,
        utility_function_name=experiment_control.experiment.utility_function_name,
        schema_pydantic_base_model_name=experiment_control.experiment.schema_pydantic_base_model_name,
        chat_history_length=experiment_control.experiment.chat_history_length,
        network_size=experiment_control.experiment.network_size,
        model_client=experiment_control.experiment.model_client,
        model_name=experiment_control.experiment.model_name,
        is_reasoning=experiment_control.experiment.is_reasoning,
        model_configs=experiment_control.experiment.model_configs,
        system_message_prompt_template_name=experiment_control.experiment.system_message_prompt_template_name,
        message_prompt_template_name=experiment_control.experiment.message_prompt_template_name,
    )
    logger.success(f"Make Experiment Configuration Files in: {experiment_control.generator.experiment_base_dir}")
    ExperimentInitializer.prepare_experiment_dir_with_index(
        experiment_base_dir=experiment_control.generator.experiment_base_dir,
        experiment_times=experiment_control.generator.experiment_times,
    )
    logger.success(f"Initialize Experiment Control Files in: {experiment_control.generator.experiment_base_dir}")


def main(
    experiment_control_file_paths: list[str],
):
    for experiment_control_file_path in experiment_control_file_paths:
        experiment_control = load_and_parse_experiment_control_file(
            experiment_control_file_path=experiment_control_file_path,
        )
        make_experiment_configuration_files(
            experiment_control=experiment_control,
        )


if __name__ == '__main__':
    logger.remove()
    logger.add(
        sink=sys.stderr,
        level='DEBUG',
    )
    main(
        experiment_control_file_paths=[
            
        ],
    )

