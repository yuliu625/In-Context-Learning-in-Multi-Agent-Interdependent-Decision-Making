from __future__ import annotations
from loguru import logger

from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from pathlib import Path

from typing import TYPE_CHECKING, Annotated, Literal
if TYPE_CHECKING:
    from langchain_core.prompts.chat import BaseMessagePromptTemplate


class PromptTemplateLoader:
    @staticmethod
    def load_prompt_template_from_j2(
        prompt_template_path: str | Path,
    ) -> PromptTemplate:
        prompt_template = PromptTemplate.from_file(
            template_file=prompt_template_path,
            template_format='jinja2',
            encoding='utf-8',
        )
        logger.debug(f"Loaded Prompt Template from: {prompt_template_path}")
        logger.debug(f"Loaded Prompt Template: \n{prompt_template}")
        return prompt_template

    @staticmethod
    def load_message_prompt_template_from_j2(
        message_prompt_template_path: str | Path,
        message_type: Literal['system', 'human', 'ai'],
    ) -> BaseMessagePromptTemplate:
        if message_type == 'system':
            return PromptTemplateLoader.load_system_message_prompt_template_from_j2(
                system_message_prompt_template_path=message_prompt_template_path,
            )
        elif message_type == 'human':
            return PromptTemplateLoader.load_human_message_prompt_template_from_j2(
                human_message_prompt_template_path=message_prompt_template_path,
            )
        elif message_type == 'ai':
            return PromptTemplateLoader.load_ai_message_prompt_template_from_j2(
                ai_message_prompt_template_path=message_prompt_template_path,
            )
        else:
            raise ValueError(f"Unsupported Message Type: {message_type}")

    @staticmethod
    def load_chat_prompt_template_from_j2(
        system_message_prompt_template_path: str | Path,
        message_place_holder_key: str = 'chat_history',
    ) -> ChatPromptTemplate:
        system_message_prompt_template = PromptTemplateLoader.load_system_message_prompt_template_from_j2(
            system_message_prompt_template_path=system_message_prompt_template_path,
        )
        chat_prompt_template = ChatPromptTemplate.from_messages(
            messages=[
                system_message_prompt_template,
                MessagesPlaceholder(message_place_holder_key),
            ],
            template_format='jinja2',
        )
        logger.debug(f"Loaded Chat Prompt Template from: {system_message_prompt_template_path}")
        logger.trace(f"Loaded Chat Prompt Template: \n{chat_prompt_template}")
        return chat_prompt_template

    @staticmethod
    def safe_load_chat_prompt_template_from_j2(
        system_message_prompt_template_path: str | Path,
        system_message_prompt_template_format_kwargs: dict,
        message_place_holder_key: str = 'chat_history',
    ) -> ChatPromptTemplate:
        system_message_prompt_template = PromptTemplateLoader.load_system_message_prompt_template_from_j2(
            system_message_prompt_template_path=system_message_prompt_template_path,
        )
        system_message = system_message_prompt_template.format(**system_message_prompt_template_format_kwargs)
        chat_prompt_template = ChatPromptTemplate.from_messages(
            messages=[
                system_message,
                MessagesPlaceholder(message_place_holder_key),
            ],
            template_format='jinja2',
        )
        logger.debug(f"Safe Loaded Chat Prompt Template from: {system_message_prompt_template_path}")
        logger.trace(f"Safe Chat Prompt Template: \n{chat_prompt_template}")
        return chat_prompt_template

    @staticmethod
    def load_system_message_prompt_template_from_j2(
        system_message_prompt_template_path: str | Path,
    ) -> SystemMessagePromptTemplate:
        template = Path(system_message_prompt_template_path).read_text(encoding='utf-8')
        system_message_prompt_template = SystemMessagePromptTemplate.from_template(
            template=template,
            template_format='jinja2',
        )
        logger.debug(f"Loaded System Message Prompt Template from: {system_message_prompt_template_path}")
        logger.trace(f"Loaded System Message Prompt Template: \n{system_message_prompt_template}")
        return system_message_prompt_template

    @staticmethod
    def load_human_message_prompt_template_from_j2(
        human_message_prompt_template_path: str | Path,
    ) -> HumanMessagePromptTemplate:
        template = Path(human_message_prompt_template_path).read_text(encoding='utf-8')
        human_message_prompt_template = HumanMessagePromptTemplate.from_template(
            template=template,
            template_format='jinja2',
        )
        logger.debug(f"Loaded Human Message Prompt Template from: {human_message_prompt_template_path}")
        logger.trace(f"Loaded Human Message Prompt Template: \n{human_message_prompt_template}")
        return human_message_prompt_template

    @staticmethod
    def load_ai_message_prompt_template_from_j2(
        ai_message_prompt_template_path: str | Path,
    ) -> AIMessagePromptTemplate:
        template = Path(ai_message_prompt_template_path).read_text(encoding='utf-8')
        ai_message_prompt_template = AIMessagePromptTemplate.from_template(
            template=template,
            template_format='jinja2',
        )
        logger.debug(f"Loaded AI Message Prompt Template from: {ai_message_prompt_template_path}")
        logger.trace(f"Loaded AI Message Prompt Template: \n{ai_message_prompt_template}")
        return ai_message_prompt_template

    @staticmethod
    def load_prompt_template_from_txt(
        prompt_template_path: str
    ) -> PromptTemplate:
        prompt_template = PromptTemplate.from_file(
            template_file=prompt_template_path,
            template_format='f-string',
            encoding='utf-8',
        )
        return prompt_template

    @staticmethod
    def load_original_txt(
        file_path: str | Path
    ) -> str:
        file_path = Path(file_path)
        text = file_path.read_text(encoding='utf-8',)
        return text

