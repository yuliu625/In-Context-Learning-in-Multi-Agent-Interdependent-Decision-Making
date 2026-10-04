from __future__ import annotations
import pytest
from loguru import logger

from src.prompts.prompt_template_factories import (
    ParticipantPromptTemplateFactory,
)

from tests.data.prompt_template_cases import (
    SYSTEM_PROMPT_TEMPLATE_NAME_CASES,
    HUMAN_PROMPT_TEMPLATE_NAME_CASES,
)

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class TestParticipantPromptTemplateFactory:
    @pytest.mark.parametrize(
        'message_prompt_template_name', SYSTEM_PROMPT_TEMPLATE_NAME_CASES,
    )
    def test_get_chat_prompt_template(
        self,
        message_prompt_template_name: str,
    ):
        participant_prompt_template_factory = ParticipantPromptTemplateFactory()
        chat_prompt_template = participant_prompt_template_factory.get_chat_prompt_template(
            system_message_prompt_template_name=message_prompt_template_name,
        )

    @pytest.mark.parametrize(
        'message_prompt_template_name', HUMAN_PROMPT_TEMPLATE_NAME_CASES,
    )
    def test_get_message_prompt_template(
        self,
        message_prompt_template_name: str,
    ):
        participant_prompt_template_factory = ParticipantPromptTemplateFactory()
        message_prompt_template = participant_prompt_template_factory.get_message_prompt_template(
            message_prompt_template_name=message_prompt_template_name,
        )

