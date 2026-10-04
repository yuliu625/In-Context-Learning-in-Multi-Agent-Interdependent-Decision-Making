from __future__ import annotations
from loguru import logger

from src.schemas.experiment_configs import (
    EnvironmentConfig,
    AgentConfig,
    StateAndMASConfigs,
)
from src.schemas.calculation_fields import (
    ExperimentResult,
)

from langchain_core.messages import (
    messages_to_dict,
    messages_from_dict,
)
import pandas as pd
import json
import jsonlines
from pathlib import Path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.mas_state import MASState
    from langchain_core.messages import AnyMessage


class StateIO:
    @staticmethod
    def load_state_and_mas_configs(
        dir_to_load_and_save: str | Path,
    ) -> StateAndMASConfigs:
        dir_to_load_and_save = Path(dir_to_load_and_save)
        environment_config_path = dir_to_load_and_save / 'environment_config.json'
        agent_configs_path = dir_to_load_and_save / 'agent_configs.jsonl'
        chat_histories_path = dir_to_load_and_save / 'chat_histories.jsonl'
        results_path = dir_to_load_and_save / 'results.jsonl'
        environment_config = StateIO.load_environment_config(
            environment_config_path=environment_config_path,
        )
        agent_configs = StateIO.load_agent_configs(
            agent_configs_path=agent_configs_path,
        )
        if chat_histories_path.exists():
            chat_histories = StateIO.load_chat_histories(
                chat_histories_path=chat_histories_path,
            )
        else:
            chat_histories = None
            logger.debug(f"Chat Histories is None")
        if results_path.exists():
            results = StateIO.load_results(
                results_path=results_path,
            )
        else:
            results = None
            logger.debug(f"Results is None")
        state_and_mas_configs = StateAndMASConfigs(
            environment_config=environment_config,
            agent_configs=agent_configs,
            chat_histories=chat_histories,
            results=results,
        )
        logger.debug(f"Loaded State and MAS Configs: {state_and_mas_configs}")
        return state_and_mas_configs

    @staticmethod
    def save_state(
        state: MASState,
        dir_to_save_result: str | Path,
    ) -> None:
        dir_to_save_result = Path(dir_to_save_result)
        chat_histories_path = dir_to_save_result / 'chat_histories.jsonl'
        results_path = dir_to_save_result / 'results.jsonl'
        StateIO.save_chat_histories(
            chat_histories=state['chat_histories'],
            chat_histories_path=chat_histories_path,
        )
        StateIO.save_results(
            results=state['results'],
            results_path=results_path,
        )
        logger.success(f"Saved state at: {results_path}")

    @staticmethod
    def load_environment_config(
        environment_config_path: str | Path,
    ) -> EnvironmentConfig:
        environment_config_path = Path(environment_config_path)
        environment_config_dict = json.loads(
            environment_config_path.read_text(
                encoding='utf-8',
            ),
        )
        environment_config = EnvironmentConfig(**environment_config_dict)
        logger.debug(f"Loaded Environment Config: {environment_config}")
        return environment_config

    @staticmethod
    def load_agent_configs(
        agent_configs_path: str | Path,
    ) -> list[AgentConfig]:
        agent_configs = []
        with jsonlines.open(agent_configs_path, 'r',) as reader:
            for obj in reader:
                agent_configs.append(
                    AgentConfig(**obj),
                )
        logger.debug(f"Loaded Agent Configs: {agent_configs}")
        return agent_configs

    @staticmethod
    def load_agent_configs_df(
        agent_configs_df_path: str | Path,
    ) -> pd.DataFrame:
        agent_configs_df_path = Path(agent_configs_df_path)
        agent_configs_df = pd.read_json(
            agent_configs_df_path,
            lines=True,
            encoding='utf-8',
        )
        logger.debug(f"Loaded Agent Configs DataFrame: \n{agent_configs_df}")
        return agent_configs_df

    @staticmethod
    def save_chat_histories(
        chat_histories: dict[str, list[AnyMessage]],
        chat_histories_path: str | Path,
    ) -> None:
        dict_to_save = {}
        for agent_id, chat_history in chat_histories.items():
            dict_to_save[agent_id] = messages_to_dict(chat_history)
        chat_histories_path = Path(chat_histories_path)
        chat_histories_path.write_text(
            json.dumps(
                dict_to_save,
                ensure_ascii=False,
            ),
            encoding='utf-8',
        )
        logger.success(f"Saved Chat Histories at: {chat_histories_path}")

    @staticmethod
    def load_chat_histories(
        chat_histories_path: str | Path,
    ) -> dict[str, list[AnyMessage]]:
        chat_histories_path = Path(chat_histories_path)
        chat_histories_dict = json.loads(
            chat_histories_path.read_text(
                encoding='utf-8',
            ),
        )
        chat_histories = {}
        for agent_id, chat_history in chat_histories_dict.items():
            chat_histories[agent_id] = messages_from_dict(chat_history)
        logger.debug(f"Loaded Chat Histories: {chat_histories}")
        return chat_histories

    @staticmethod
    def save_results(
        results: list[ExperimentResult],
        results_path: str | Path,
    ) -> None:
        results_ = [result.model_dump() for result in results]
        with jsonlines.open(results_path, 'w', dumps=lambda obj: json.dumps(obj, ensure_ascii=False,),) as writer:
            writer.write_all(results_)
        logger.success(f"Saved Results at: {results_path}")

    @staticmethod
    def load_results(
        results_path: str | Path,
    ) -> list[ExperimentResult]:
        results = []
        with jsonlines.open(results_path, 'r',) as reader:
            for obj in reader:
                results.append(
                    ExperimentResult(**obj),
                )
        logger.debug(f"Loaded Results: {results}")
        return results

    @staticmethod
    def save_results_df(
        results_df: pd.DataFrame,
        results_df_path: str | Path,
    ) -> None:
        results_df.to_json(
            results_df_path,
            orient='records',
            lines=True,
            force_ascii=False,
        )
        logger.success(f"Saved Results at: {results_df_path}")

    @staticmethod
    def load_results_df(
        results_df_path: str | Path,
    ) -> pd.DataFrame:
        results_df = pd.read_json(
            results_df_path,
            orient='records',
            lines=True,
            encoding='utf-8',
        )
        logger.debug(f"Loaded Results: {results_df}")
        return results_df

