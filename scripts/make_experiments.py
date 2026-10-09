from __future__ import annotations
import sys
from loguru import logger

from src.configurations.configuration_generator import ConfigurationGenerator

from pathlib import Path

from typing import TYPE_CHECKING, Literal
# if TYPE_CHECKING:


def make_experiment_control_files(
    experiment_control_template_file_path: str | Path,
    experiment_control_file_path: str | Path,
    experiment_root_dir: str,
    experiment_name: str,
    experiment_times: int,
    network_effect: float,
    prices: list[float],
    utility_function_name: Literal[
        'linear',
    ],
    schema_pydantic_base_model_name: Literal[
        'all', 'only-expectation', 'only-choice',
    ],
    chat_history_length: int,
    network_size: int,
    model_client: Literal[
        'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
    ],
    model_name: str,
    is_reasoning: bool,
    model_configs: dict,
    system_message_prompt_template_name: str,
    message_prompt_template_name: str,
) -> Path:
    experiment_control_file_path = Path(experiment_control_file_path)
    experiment_control_file_path.parent.mkdir(parents=True, exist_ok=True,)
    ConfigurationGenerator.make_experiment_control_file(
        experiment_control_template_file_path=experiment_control_template_file_path,
        persistence_config_kwargs=dict(
            experiment_root_dir=experiment_root_dir,
            experiment_name=experiment_name,
            experiment_times=experiment_times,
        ),
        runtime_config_kwargs=dict(
            network_effect=network_effect,
            prices=prices,
            utility_function_name=utility_function_name,
            schema_pydantic_base_model_name=schema_pydantic_base_model_name,
            chat_history_length=chat_history_length,
            network_size=network_size,
            model_client=model_client,
            model_name=model_name,
            is_reasoning=is_reasoning,
            model_configs=model_configs,
            system_message_prompt_template_name=system_message_prompt_template_name,
            message_prompt_template_name=message_prompt_template_name,
        ),
        experiment_control_file_path=experiment_control_file_path,
    )
    logger.success(f"Saved Experiment Control File at: {experiment_control_file_path}")
    return Path(experiment_control_file_path)


def main():
    """
    This script programmatically generates standardized build configuration files that conform to the predefined schema.

    Alternatively, this script may be bypassed, and the configuration files can be manually authored, provided that they satisfy the same schema.
    """


if __name__ == '__main__':
    logger.remove()
    logger.add(
        sink=sys.stderr,
        level='DEBUG',
    )
    main()

