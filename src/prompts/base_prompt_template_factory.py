from __future__ import annotations
from loguru import logger

from src.prompts.prompt_template_loader import PromptTemplateLoader

from pathlib import Path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from langchain_core.prompts import (
        PromptTemplate,
        ChatPromptTemplate,
        HumanMessagePromptTemplate,
    )


class BasePromptTemplateFactory:
    def __init__(
        self,
        prompt_templates_dir: str | Path | None = None,
    ):
        if prompt_templates_dir is None:
            self.prompt_templates_dir = Path(__file__).parent
        else:
            self.prompt_templates_dir = Path(prompt_templates_dir)

    def get_chat_prompt_template(
        self,
        system_message_prompt_template_name: str,
    ) -> ChatPromptTemplate:
        system_message_prompt_template_path = (
            self.prompt_templates_dir
            / f"system_message_prompt_template_{system_message_prompt_template_name}.j2"
        )
        chat_prompt_template = PromptTemplateLoader.load_chat_prompt_template_from_j2(
            system_message_prompt_template_path=system_message_prompt_template_path
        )
        return chat_prompt_template

    def safe_get_chat_prompt_template(
        self,
        system_message_prompt_template_name: str,
        system_message_prompt_template_format_kwargs: dict | None = None,
    ) -> ChatPromptTemplate:
        system_message_prompt_template_path = (
            self.prompt_templates_dir
            / f"system_message_prompt_template_{system_message_prompt_template_name}.j2"
        )
        chat_prompt_template = PromptTemplateLoader.safe_load_chat_prompt_template_from_j2(
            system_message_prompt_template_path=system_message_prompt_template_path,
            system_message_prompt_template_format_kwargs=system_message_prompt_template_format_kwargs,
        )
        return chat_prompt_template

    def get_message_prompt_template(
        self,
        message_prompt_template_name: str,
    ) -> HumanMessagePromptTemplate:
        human_message_prompt_template_path = (
            self.prompt_templates_dir
            / f"human_message_prompt_template_{message_prompt_template_name}.j2"
        )
        message_prompt_template = PromptTemplateLoader.load_human_message_prompt_template_from_j2(
            human_message_prompt_template_path=human_message_prompt_template_path,
        )
        return message_prompt_template

    def get_prompt_template(
        self,
        prompt_template_name: str,
    ) -> PromptTemplate:
        prompt_template_path = self.prompt_templates_dir / f"{prompt_template_name}.j2"
        prompt_template = PromptTemplateLoader.load_prompt_template_from_j2(
            prompt_template_path=prompt_template_path,
        )
        return prompt_template

    def set_sub_dir(
        self,
        sub_dir: str | Path
    ) -> None:
        sub_dir = Path(sub_dir)
        self.prompt_templates_dir = self.prompt_templates_dir / sub_dir
        logger.info(f"Set Prompt Template Directory: {self.prompt_templates_dir}")

