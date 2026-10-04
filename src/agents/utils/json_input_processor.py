from __future__ import annotations
from loguru import logger

import json

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class JsonInputProcessor:
    @staticmethod
    def put_in_markdown(
        original_structured_data: dict | list,
    ) -> str:
        json_str = JsonInputProcessor.get_json_str_from_python_structured_data(
            original_structured_data=original_structured_data,
        )
        result = JsonInputProcessor.wrap_in_markdown_code_cell(
            json_str=json_str,
        )
        logger.debug(f"Processed Result: {result}")
        return result

    @staticmethod
    def get_json_str_from_python_structured_data(
        original_structured_data: dict | list
    ) -> str:
        json_str = json.dumps(
            original_structured_data,
            ensure_ascii=False,
        )
        logger.trace(f"Json String: {json_str}")
        return json_str

    @staticmethod
    def wrap_in_markdown_code_cell(
        json_str: str
    ) -> str:
        result_str = f"```json\n{json_str}\n```"
        logger.trace(f"Result String: {result_str}")
        return result_str

    @staticmethod
    def _escape_braces(
        string: str
    ) -> str:
        string = string.replace("{", "{{").replace("}", "}}")
        return string

