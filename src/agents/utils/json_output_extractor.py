from __future__ import annotations
from loguru import logger

import json
import json5
import json_repair
import re

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from pydantic import BaseModel


class JsonOutputExtractor:
    @staticmethod
    def extract_json_from_str(
        raw_str: str,
        index_to_choose: int = -1,
        json_loader_name: Literal[
            'json', 'json5', 'json-repair',
        ] = 'json-repair',
        schema_pydantic_base_model: type[BaseModel] | None = None,
        schema_check_type: Literal[
            'dict', 'list',
        ] = 'dict',
    ) -> dict | list | None:
        raw_json_str = JsonOutputExtractor.re_match(
            raw_str=raw_str,
            index_to_choose=index_to_choose,
        )
        if not raw_json_str:
            return None
        raw_structured_data = JsonOutputExtractor.load_structured_data_from_raw_json_str(
            raw_json_str=raw_json_str,
            json_loader_name=json_loader_name,
        )
        if not raw_structured_data:
            return None
        if schema_pydantic_base_model:
            if schema_check_type == 'dict' and not JsonOutputExtractor.check_dict_schema(
                raw_dict_structured_data=raw_structured_data,
                schema_pydantic_base_model=schema_pydantic_base_model,
            ):
                return None
            elif schema_check_type == 'list' and not JsonOutputExtractor.check_list_schema(
                raw_list_structured_data=raw_structured_data,
                schema_pydantic_base_model=schema_pydantic_base_model,
            ):
                return None
        return raw_structured_data

    @staticmethod
    def re_match(
        raw_str: str,
        index_to_choose: int = -1
    ) -> str | None:
        pattern = r'```json(.*?)```'
        matches = re.findall(pattern, raw_str, re.DOTALL,)
        if not matches:
            logger.error("No JSON outputs.")
            return None
        raw_json_str: str = matches[index_to_choose]
        return raw_json_str

    @staticmethod
    def load_structured_data_from_raw_json_str(
        raw_json_str: str,
        json_loader_name: Literal[
            'json', 'json5', 'json-repair',
        ] = 'json-repair',
    ) -> dict | list | None:
        try:
            if json_loader_name == 'json':
                return json.loads(raw_json_str)
            elif json_loader_name == 'json5':
                return json5.loads(raw_json_str)
            elif json_loader_name == 'json-repair':
                return json_repair.loads(raw_json_str)
        except Exception as e:
            logger.error(e)
            logger.error(raw_json_str)
            return None

    @staticmethod
    def check_dict_schema(
        raw_dict_structured_data: dict,
        schema_pydantic_base_model: type[BaseModel],
    ) -> dict | None:
        if not isinstance(raw_dict_structured_data, dict):
            return None
        try:
            schema_pydantic_base_model(**raw_dict_structured_data)
        except Exception as e:
            logger.error(e)
            logger.error(raw_dict_structured_data)
            return None
        return raw_dict_structured_data

    @staticmethod
    def check_list_schema(
        raw_list_structured_data: list,
        schema_pydantic_base_model: type[BaseModel],
    ) -> list | None:
        if not isinstance(raw_list_structured_data, list):
            return None
        try:
            schema_pydantic_base_model(items=raw_list_structured_data)
        except Exception as e:
            logger.error(e)
            logger.error(raw_list_structured_data)
            return None
        return raw_list_structured_data

    @staticmethod
    def delete_last_json(
        text: str
    ) -> str:
        pattern = r'```json(.*?)```'
        matches = list(re.finditer(pattern, text, re.DOTALL,))
        last = matches[-1]
        start, end = last.span()
        return text[:start] + text[end:]

