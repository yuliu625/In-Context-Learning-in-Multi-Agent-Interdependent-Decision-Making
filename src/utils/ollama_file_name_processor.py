from __future__ import annotations
from loguru import logger

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class OllamaFileNameProcessor:
    @staticmethod
    def encode_filename(
        name: str,
    ) -> str:
        encoded_name = name.replace('.', '_DOT_')
        encoded_name = encoded_name.replace(':', '_COLON_')
        return encoded_name

    @staticmethod
    def decode_filename(
        encoded_name: str,
    ) -> str:
        decoded_name = encoded_name.replace('_DOT_', '.')
        decoded_name = decoded_name.replace('_COLON_', ':')
        return decoded_name

