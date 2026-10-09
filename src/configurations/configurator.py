from __future__ import annotations
from loguru import logger

from src.schemas.experiment_configs import (
    EnvironmentConfig,
    AgentConfig,
)

import pandas as pd
import json
import jsonlines
from pathlib import Path

from typing import TYPE_CHECKING, Literal
# if TYPE_CHECKING:


class Configurator:
    @staticmethod
    def make_default_configuration_files(
        dir_to_load_and_save: str | Path,
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
    ) -> None:
        dir_to_load_and_save = Path(dir_to_load_and_save)
        dir_to_load_and_save.mkdir(parents=True, exist_ok=True, )
        path_to_environment_config = dir_to_load_and_save / 'environment_config.json'
        path_to_agent_configs = dir_to_load_and_save / 'agent_configs.jsonl'
        environment_config = EnvironmentConfig(
            network_effect=network_effect,
            prices=prices,
            utility_function_name=utility_function_name,
            schema_pydantic_base_model_name=schema_pydantic_base_model_name,
            chat_history_length=chat_history_length,
        ).model_dump()
        logger.trace(f"environment_config: {environment_config}")
        agent_configs = [
            AgentConfig(
                agent_id=f'agent_{i}',
                model_client=model_client,
                model_name=model_name,
                is_reasoning=is_reasoning,
                model_configs=model_configs,
                standalone_value=i,
                system_message_prompt_template_name=system_message_prompt_template_name,
                message_prompt_template_name=message_prompt_template_name,
            ).model_dump()
            for i in range(network_size)
        ]
        logger.trace(f"agent_configs: {agent_configs}")
        path_to_environment_config.write_text(
            json.dumps(environment_config, ensure_ascii=False,),
            encoding='utf-8',
        )
        logger.success(f"Save Environment Config to: {path_to_environment_config}")
        with jsonlines.open(path_to_agent_configs, 'w', dumps=lambda obj: json.dumps(obj, ensure_ascii=False,),) as writer:
            writer.write_all(agent_configs)
        logger.success(f"Save Agent Configs to: {path_to_agent_configs}")

    @staticmethod
    def agent_configs_from_jsonl_to_excel(
        experiment_base_dir: str | Path,
    ) -> None:
        agent_configs_jsonl_path = Path(experiment_base_dir) / 'agent_configs.jsonl'
        df = pd.read_json(
            agent_configs_jsonl_path,
            orient='records',
            lines=True,
            encoding='utf-8',
        )
        df.to_excel(
            agent_configs_jsonl_path.with_suffix('.xlsx'),
            index=False,
        )
        logger.success(f"Save Agent Configs to: {agent_configs_jsonl_path.with_suffix('.xlsx')}")

    @staticmethod
    def agent_configs_from_excel_to_jsonl(
        experiment_base_dir: str | Path,
    ) -> None:
        agent_configs_xlsx_path = Path(experiment_base_dir) / 'agent_configs.xlsx'
        df = pd.read_excel(
            agent_configs_xlsx_path,
        )
        df.to_json(
            agent_configs_xlsx_path.with_suffix('.jsonl'),
            orient='records',
            lines=True,
            force_ascii=False,
        )
        logger.success(f"Save Agent Configs to: {agent_configs_xlsx_path.with_suffix('.jsonl')}")

