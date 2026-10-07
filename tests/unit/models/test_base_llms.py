from __future__ import annotations
import pytest
from loguru import logger

from src.models.base_llm_factory import (
    BaseLLMFactory,
)

from tests.data.human_message_cases import (
    HUMAN_MESSAGE_CONTENT_CASES,
)

from langchain_core.messages import AIMessage

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestBaseLLMs:
    @pytest.mark.parametrize(
        'model_name, messages', [
            ('gpt-4o-mini', HUMAN_MESSAGE_CONTENT_CASES),
        ])
    def test_openai_llm(self, model_name, messages):
        llm = BaseLLMFactory.create_openai_llm(
            model_name=model_name,
        )
        for human_message in messages:
            response = llm.invoke(human_message)
            logger.info(response)
            assert isinstance(response, AIMessage)

    @pytest.mark.parametrize(
        'model_name, messages', [
            ('gemini-2.5-flash', HUMAN_MESSAGE_CONTENT_CASES),
        ])
    def test_google_llm(self, model_name, messages):
        llm = BaseLLMFactory.create_google_llm(
            model_name=model_name,
            model_configs={'include_thoughts': True},
        )
        for human_message in messages:
            response = llm.invoke(human_message)
            logger.info(response)
            assert isinstance(response, AIMessage)

    @pytest.mark.parametrize(
        'model_name, messages', [
            ('claude-opus-4', HUMAN_MESSAGE_CONTENT_CASES),
        ])
    def test_anthropic_llm(self, model_name, messages):
        llm = BaseLLMFactory.create_anthropic_llm(
            model_name=model_name,
        )
        for human_message in messages:
            response = llm.invoke(human_message)
            logger.info(response)
            assert isinstance(response, AIMessage)

    @pytest.mark.parametrize(
        'model_name, messages', [
            ('qwen-turbo', HUMAN_MESSAGE_CONTENT_CASES),
        ])
    def test_dashscope_llm(self, model_name, messages):
        llm = BaseLLMFactory.create_dashscope_llm(
            model_name=model_name,
        )
        for human_message in messages:
            response = llm.invoke(human_message)
            logger.info(response)
            assert isinstance(response, AIMessage)

    @pytest.mark.parametrize(
        'model_name, messages', [
            ('deepseek-r1', HUMAN_MESSAGE_CONTENT_CASES),
        ])
    def test_deepseek_llm(self, model_name, messages):
        llm = BaseLLMFactory.create_deepseek_llm(
            model_name=model_name,
        )
        for human_message in messages:
            response = llm.invoke(human_message)
            logger.info(response)
            assert isinstance(response, AIMessage)

    @pytest.mark.parametrize(
        'model_name, messages', [
            ('qwen2.5:0.5b', HUMAN_MESSAGE_CONTENT_CASES),
        ]
    )
    def test_ollama_llm(self, model_name, messages):
        llm = BaseLLMFactory.create_ollama_llm(
            model_name=model_name,
        )
        for human_message in messages:
            response = llm.invoke(human_message)
            logger.info(response)
            assert isinstance(response, AIMessage)

