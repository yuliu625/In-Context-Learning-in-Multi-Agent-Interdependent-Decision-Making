from __future__ import annotations
from loguru import logger

from src.schemas.calculation_fields import (
    ExperimentResult,
)
from src.schemas.structured_output_format import (
    StructuredOutputFormatFactory,
)
from src.agents.utils.json_output_extractor import JsonOutputExtractor
from src.io.state_io import StateIO

import pandas as pd
from pathlib import Path
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
)

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from langchain_core.messages import AnyMessage


class ResultProcessor:
    @staticmethod
    def merge_results_and_chat_histories(
        dir_to_load_and_save: str | Path,
    ) -> pd.DataFrame:
        dir_to_load_and_save = Path(dir_to_load_and_save)
        state_and_mas_configs = StateIO.load_state_and_mas_configs(
            dir_to_load_and_save=dir_to_load_and_save,
        )
        chat_histories_df = ResultProcessor.convert_chat_histories_df(
            chat_histories=state_and_mas_configs.chat_histories,
        )
        results_df = ResultProcessor.convert_results_df(
            results=state_and_mas_configs.results,
        )
        all_in_one_df = pd.merge(
            results_df,
            chat_histories_df,
            how='inner',
            on=['experiment_round', 'agent_id'],
        )
        logger.trace(f"all_in_one_df: \n{all_in_one_df}")
        all_in_one_path = dir_to_load_and_save / 'all_in_one.xlsx'
        try:
            all_in_one_df.to_excel(
                all_in_one_path.with_suffix('.xlsx'),
                index=False,
            )
            logger.success(f"Saved all_in_one.xlsx at: {all_in_one_path.with_suffix('.xlsx')}")
        except Exception as e:
            logger.error(e)
        all_in_one_df.to_json(
            all_in_one_path.with_suffix('.jsonl'),
            index=False,
            orient='records',
            lines=True,
            force_ascii=False,
        )
        logger.success(f"Saved all_in_one.jsonl at: {all_in_one_path.with_suffix('.jsonl')}")
        return all_in_one_df

    @staticmethod
    def convert_results_df(
        results: list[ExperimentResult],
    ) -> pd.DataFrame:
        results_ = [result.model_dump() for result in results]
        results_df = pd.DataFrame(results_)
        logger.trace(f"results_df: \n{results_df}")
        return results_df

    @staticmethod
    def parse_results_df_via_chat_histories(
        chat_histories: dict[str, list[AnyMessage]],
    ) -> pd.DataFrame:
        raise NotImplementedError

    @staticmethod
    def convert_chat_histories_df(
        chat_histories: dict[str, list[AnyMessage]],
    ) -> pd.DataFrame:
        agent_chat_history_dfs = []
        for agent_id, chat_history in chat_histories.items():
            agent_chat_history_df = ResultProcessor.convert_agent_chat_history_df(
                agent_chat_history=chat_history,
            )
            agent_chat_history_df['agent_id'] = agent_id
            agent_chat_history_dfs.append(agent_chat_history_df)
        chat_histories_df = pd.concat(
            agent_chat_history_dfs,
            ignore_index=True,
        )
        logger.trace(f"chat_histories_df: \n{chat_histories_df}")
        return chat_histories_df

    @staticmethod
    def convert_agent_chat_history_df(
        agent_chat_history: list[AnyMessage],
    ) -> pd.DataFrame:
        agent_chat_history_data = []
        for i in range(0, len(agent_chat_history), 2):
            human_message = agent_chat_history[i]
            ai_message = agent_chat_history[i + 1]
            assert isinstance(human_message, HumanMessage)
            assert isinstance(ai_message, AIMessage)
            agent_chat_history_data.append(dict(
                experiment_round=i//2,
                environment_message=human_message.content,
                agent_message=ai_message.content,
                reasoning_content=ResultProcessor.extract_reasoning_content(
                    ai_message=ai_message,
                ),
                agent_reason=JsonOutputExtractor.extract_json_from_str(
                    raw_str=ai_message.content,
                    index_to_choose=-1,
                    json_loader_name='json-repair',
                    schema_pydantic_base_model=StructuredOutputFormatFactory.create_structured_output_format(
                        schema_pydantic_base_model_name='only-expectation',
                    ),
                    schema_check_type='dict',
                )['reason'],
            ))
        agent_chat_history_df = pd.DataFrame(agent_chat_history_data)
        logger.trace(f"agent_chat_history_df: \n{agent_chat_history_df}")
        return agent_chat_history_df

    @staticmethod
    def extract_reasoning_content(
        ai_message: AIMessage,
    ) -> str:
        return ai_message.additional_kwargs.get('reasoning_content', "")

    @staticmethod
    def parse_token_number(
        ai_message: AIMessage,
    ) -> int:
        token_number = ai_message.usage_metadata.get('output_tokens')
        if token_number:
            token_number = ai_message.usage_metadata.get('output_tokens')
        else:
            token_number = ai_message.response_metadata['token_usage'].get('completion_tokens')
        if token_number is None:
            token_number = ai_message.response_metadata['token_usage'].get('output_tokens')
        if token_number is None:
            token_number = 0
        return token_number

