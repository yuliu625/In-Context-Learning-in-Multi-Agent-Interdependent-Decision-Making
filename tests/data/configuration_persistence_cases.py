from __future__ import annotations
from loguru import logger

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


EXPERIMENT_CONFIGURATION_DICT_CASES = [
    dict(
        network_effect=0.5,
        prices=[3.0, 5.0,],
        utility_function_name='linear',
        schema_pydantic_base_model_name='only-expectation',
        chat_history_length=10,
        network_size=6,
        model_client='ollama',
        model_name='qwen2.5:0.5b',
        is_reasoning=False,
        model_configs=dict(),
        system_message_prompt_template_name='demo',
        message_prompt_template_name='demo',
    ),
]


EXPERIMENT_PATH_DICT_CASES = [
    dict(
        experiment_root_dir="fake_experiment_root_dir",
        experiment_name="fake_experiment_name",
        experiment_times=3,
    ),
]

