from __future__ import annotations
from loguru import logger

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
)

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from langchain_core.messages import BaseMessage


class MessageCopier:
    @staticmethod
    def auto_copy_message(
        original_message: BaseMessage,
    ) -> AIMessage | HumanMessage:
        message_dict = original_message.model_dump()
        if isinstance(original_message, AIMessage):
            ai_message = AIMessage(**message_dict)
            logger.trace(f"Copied AI Message: {ai_message}")
            return ai_message
        elif isinstance(original_message, HumanMessage):
            human_message = HumanMessage(**message_dict)
            logger.trace(f"Copied Human Message: {human_message}")
            return human_message
        else:
            raise TypeError(f"Unsupported Message Type: {type(original_message)}")

    @staticmethod
    def copy_message(
        original_message: BaseMessage,
        output_message_type: Literal[
            'ai_message',
            'human_message',
        ],
    ) -> AIMessage | HumanMessage:
        message_dict = original_message.model_dump()
        if output_message_type == 'ai_message':
            ai_message = AIMessage(**message_dict)
            logger.trace(f"Copied AI Message: {ai_message}")
            return ai_message
        elif output_message_type == 'human_message':
            human_message = HumanMessage(**message_dict)
            logger.trace(f"Copied Human Message: {human_message}")
            return human_message
        else:
            raise TypeError(f"Unsupported Message Type: {type(original_message)}")

