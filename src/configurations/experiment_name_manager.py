from __future__ import annotations
from loguru import logger

from typing import TYPE_CHECKING, Literal
# if TYPE_CHECKING:


class ExperimentNameManager:
    @staticmethod
    def make_experiment_name(
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
        model_name: str,
        network_size: int,
        experiment_tag: str,
    ) -> str:
        experiment_name = (
            f"model-client-{model_client}--model-name-{model_name}"
            '--'
            f'network-size-{network_size}'
            '--'
            f'experiment-tag-{experiment_tag}'
        )
        logger.trace(f"Experiment Name: {experiment_name}")
        return experiment_name

