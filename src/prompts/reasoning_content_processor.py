from __future__ import annotations
from loguru import logger

import re
from langchain_core.messages import AIMessage

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class ReasoningContentProcessor:
    @staticmethod
    def thinking_to_reasoning(
        ai_message: AIMessage,
        tag: str = 'think',
    ) -> AIMessage:
        thinking_content = ReasoningContentProcessor.extract_thinking_content_from_message_content(
            ai_message=ai_message,
            tag=tag,
        )
        normal_content = ReasoningContentProcessor.get_normal_content_without_thinking_content(
            ai_message=ai_message,
            tag=tag,
        )
        ai_message.additional_kwargs['reasoning_content'] = thinking_content
        ai_message.content = normal_content
        logger.debug(f"Processed AI Message: {ai_message}")
        return ai_message

    @staticmethod
    def reasoning_to_thinking(
        ai_message: AIMessage,
        tag: str = 'think',
    ) -> AIMessage:
        raise NotImplementedError

    @staticmethod
    def extract_reasoning_content_from_addition_kwargs(
        ai_message: AIMessage,
    ) -> str:
        reasoning_content = ai_message.additional_kwargs.get('reasoning_content', "")
        logger.trace(f"Reasoning Content: {reasoning_content}")
        return reasoning_content

    @staticmethod
    def extract_thinking_content_from_message_content(
        ai_message: AIMessage,
        tag: str = 'think',
    ) -> str:
        pattern = rf'<{tag}>(.*?)</{tag}>'
        matches = re.findall(pattern, ai_message.content, re.DOTALL,)
        if not matches:
            logger.trace(f"No Thinking Content")
            return ""
        logger.trace(f"Thinking Content: {matches[0]}")
        return matches[0]

    @staticmethod
    def get_normal_content_without_thinking_content(
        ai_message: AIMessage,
        tag: str = 'think',
    ) -> str:
        pattern = rf'<{tag}>(.*?)</{tag}>'
        cleaned_text = re.sub(pattern, '', ai_message.content, flags=re.DOTALL,)
        logger.trace(f"Cleaned Content: {cleaned_text}")
        return cleaned_text

