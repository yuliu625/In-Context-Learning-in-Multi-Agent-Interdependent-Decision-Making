from __future__ import annotations
from loguru import logger

from src.configs import FORMAT_MAX_RETRIES
from src.agents.interfaces.ne_base_agents import NEBaseAgent
from src.prompts.message_copier import MessageCopier
from src.prompts.reasoning_content_processor import ReasoningContentProcessor

from langchain_core.messages import message_chunk_to_message
from langchain_core.messages import AIMessage

from typing import TYPE_CHECKING, cast
if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.messages import AnyMessage, AIMessageChunk
    from pydantic import BaseModel


class ReasoningOpenAIAgent(NEBaseAgent):
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


class ReasoningGoogleAgent(NEBaseAgent):
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

    async def a_call_llm(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        chat_history: list[AnyMessage],
    ) -> AIMessage:
        llm_chain = chat_prompt_template | llm
        response = await llm_chain.ainvoke(
            input={'chat_history': chat_history},
        )
        assert isinstance(response, AIMessage)
        response = self.process_gemini_reasoning_content(
            original_message=response,
        )
        return response

    def process_gemini_reasoning_content(
        self,
        original_message: AIMessage,
    ) -> AIMessage:
        processed_message = MessageCopier.auto_copy_message(original_message)
        assert isinstance(processed_message, AIMessage)
        if isinstance(original_message.content, str):
            return processed_message
        elif isinstance(original_message.content, list):
            processed_message.content = original_message.content[1]
            processed_message.additional_kwargs['reasoning_content'] = original_message.content[0].get('thinking', "")
            return processed_message


class ReasoningAnthropicAgent(NEBaseAgent):
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
        raise NotImplementedError


class ReasoningDashScopeAgent(NEBaseAgent):
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

    async def a_call_llm(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        chat_history: list[AnyMessage],
    ) -> AIMessage:
        llm_chain = chat_prompt_template | llm
        chunks = []
        async for chunk in llm_chain.astream(
            input={'chat_history': chat_history},
        ):
            chunks.append(chunk)
        response = message_chunk_to_message(
            cast('AIMessageChunk', sum(chunks, chunks[0]))
        )
        assert isinstance(response, AIMessage)
        return response


class ReasoningDeepSeekAgent(NEBaseAgent):
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


class ReasoningOllamaAgent(NEBaseAgent):
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

