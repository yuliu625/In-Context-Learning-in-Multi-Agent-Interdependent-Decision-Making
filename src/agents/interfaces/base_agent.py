from __future__ import annotations
from loguru import logger

from src.agents.utils.json_output_extractor import JsonOutputExtractor
from src.schemas.interaction_protocols import AgentResponse

from langchain_core.messages import AIMessage
from collections import Counter

from typing import TYPE_CHECKING, Literal, Self, cast
if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig
    from langchain_core.language_models import BaseChatModel
    from langchain_core.messages import AnyMessage
    from langchain_core.prompts import ChatPromptTemplate
    from pydantic import BaseModel


class BaseAgent:
    def __init__(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        max_retries: int = 10,
        is_need_structured_output: bool = False,
        schema_pydantic_base_model: type[BaseModel] | None = None,
        schema_check_type: Literal['dict', 'list'] = 'dict',
    ):
        self._chat_prompt_template = chat_prompt_template
        self._llm = llm
        self._max_retries = max_retries
        self._is_need_structured_output = is_need_structured_output
        self._schema_pydantic_base_model = schema_pydantic_base_model
        self._schema_check_type = schema_check_type

    def process_state(
        self,
        state,
        config: RunnableConfig,
    ) -> dict:
        raise NotImplementedError

    def call_llm(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        chat_history: list[AnyMessage],
    ) -> AIMessage:
        llm_chain = chat_prompt_template | llm
        response = llm_chain.invoke(input={'chat_history': chat_history})
        assert isinstance(response, AIMessage)
        logger.trace(f"LLM Response: {response}")
        return response

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
        logger.trace(f"LLM Response: {response}")
        return response

    def call_llm_with_retry(
        self,
        chat_history: list[AnyMessage],
    ) -> AIMessage:
        if not self._is_need_structured_output:
            return self.call_llm(
                chat_prompt_template=self._chat_prompt_template,
                llm=self._llm,
                chat_history=chat_history,
            )
        for _ in range(self._max_retries):
            response = self.call_llm(
                chat_prompt_template=self._chat_prompt_template,
                llm=self._llm,
                chat_history=chat_history,
            )
            if self.get_structured_output(raw_str=response.content):
                return response
        raise RuntimeError

    async def a_call_llm_with_retry(
        self,
        chat_history: list[AnyMessage],
    ) -> AIMessage:
        if not self._is_need_structured_output:
            return await self.a_call_llm(
                chat_prompt_template=self._chat_prompt_template,
                llm=self._llm,
                chat_history=chat_history,
            )
        for _ in range(self._max_retries):
            response = await self.a_call_llm(
                chat_prompt_template=self._chat_prompt_template,
                llm=self._llm,
                chat_history=chat_history,
            )
            if self.get_structured_output(raw_str=response.content):
                return response
        raise RuntimeError

    def get_structured_output(
        self,
        raw_str: str,
    ) -> dict | list | None:
        return JsonOutputExtractor.extract_json_from_str(
            raw_str=raw_str,
            index_to_choose=-1,
            json_loader_name='json-repair',
            schema_pydantic_base_model=self._schema_pydantic_base_model,
            schema_check_type=self._schema_check_type,
        )

    def format_system_prompt_template(
        self,
        format_kwargs: dict,
    ) -> Self:
        system_message_prompt_template_input_variables = list(self._chat_prompt_template.input_variables)
        system_message_prompt_template_input_variables.remove('chat_history')
        assert Counter(system_message_prompt_template_input_variables) == Counter(list(format_kwargs.keys()))
        self._chat_prompt_template = self._chat_prompt_template.partial(**format_kwargs)
        logger.debug(f"System Message Prompt Template is formatted.")
        logger.trace(f"Chat Prompt Template: {self._chat_prompt_template}")
        return self

