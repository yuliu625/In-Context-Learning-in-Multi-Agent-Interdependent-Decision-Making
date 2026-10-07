from __future__ import annotations
from loguru import logger

from src.configs import FORMAT_MAX_RETRIES
from src.agents.interfaces.ne_base_agents import NEBaseAgent

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel
    from langchain_core.prompts import ChatPromptTemplate
    from pydantic import BaseModel


class NormalAgent(NEBaseAgent):
    def __init__(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ):
        super().__init__(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            max_retries=FORMAT_MAX_RETRIES,
            is_need_structured_output=True,
            schema_pydantic_base_model=schema_pydantic_base_model,
            schema_check_type='dict',
        )
        logger.debug(f"Created Normal Agent.")


class NormalOpenAIAgent(NEBaseAgent):
    def __init__(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ):
        super().__init__(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            max_retries=FORMAT_MAX_RETRIES,
            is_need_structured_output=True,
            schema_pydantic_base_model=schema_pydantic_base_model,
            schema_check_type='dict',
        )


class NormalGoogleAgent(NEBaseAgent):
    def __init__(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ):
        super().__init__(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            max_retries=FORMAT_MAX_RETRIES,
            is_need_structured_output=True,
            schema_pydantic_base_model=schema_pydantic_base_model,
            schema_check_type='dict',
        )


class NormalAnthropicAgent(NEBaseAgent):
    def __init__(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ):
        super().__init__(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            max_retries=FORMAT_MAX_RETRIES,
            is_need_structured_output=True,
            schema_pydantic_base_model=schema_pydantic_base_model,
            schema_check_type='dict',
        )


class NormalDashScopeAgent(NEBaseAgent):
    def __init__(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ):
        super().__init__(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            max_retries=FORMAT_MAX_RETRIES,
            is_need_structured_output=True,
            schema_pydantic_base_model=schema_pydantic_base_model,
            schema_check_type='dict',
        )


class NormalDeepSeekAgent(NEBaseAgent):
    def __init__(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ):
        super().__init__(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            max_retries=FORMAT_MAX_RETRIES,
            is_need_structured_output=True,
            schema_pydantic_base_model=schema_pydantic_base_model,
            schema_check_type='dict',
        )


class NormalOllamaAgent(NEBaseAgent):
    def __init__(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ):
        super().__init__(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            max_retries=FORMAT_MAX_RETRIES,
            is_need_structured_output=True,
            schema_pydantic_base_model=schema_pydantic_base_model,
            schema_check_type='dict',
        )

