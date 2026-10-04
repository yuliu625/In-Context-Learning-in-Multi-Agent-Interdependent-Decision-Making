from __future__ import annotations
from loguru import logger

from src.prompts.base_prompt_template_factory import BasePromptTemplateFactory

from typing import TYPE_CHECKING, Literal
# if TYPE_CHECKING:
#     from langchain_core.messages import BaseMessage


class ParticipantPromptTemplateFactory(BasePromptTemplateFactory):
    def __init__(
        self,
    ):
        super().__init__()
        logger.info(f"Build Participant Prompt Template Factory.")
        self.set_sub_dir('../../configs/participants')

