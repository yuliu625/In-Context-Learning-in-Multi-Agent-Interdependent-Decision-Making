from __future__ import annotations
from loguru import logger

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from langchain_core.prompts.message import BaseMessagePromptTemplate


def safe_format_message_prompt_template(
    message_prompt_templates: list[BaseMessagePromptTemplate | BaseMessage],
    format_kwargs: dict,
) -> list[BaseMessage]:
    chat_prompt_template = ChatPromptTemplate(
        messages=message_prompt_templates,
    )
    logger.trace(f"Format kwargs: {format_kwargs}")
    chat_prompt_value = chat_prompt_template.invoke(input=format_kwargs)
    messages = chat_prompt_value.to_messages()
    assert all(
        isinstance(message, BaseMessage)
        for message in messages
    )
    logger.trace(f"Messages: \n{messages}")
    return messages

