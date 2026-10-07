from __future__ import annotations
from loguru import logger

from src.agents.interfaces.base_agent import BaseAgent
from src.schemas.interaction_protocols import AgentResponse

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig
    from langchain_core.language_models import BaseChatModel
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.messages import AnyMessage
    from pydantic import BaseModel


class NEBaseAgent(BaseAgent):
    def __init__(
        self,
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        max_retries: int = 10,
        is_need_structured_output: bool = False,
        schema_pydantic_base_model: type[BaseModel] | None = None,
        schema_check_type: Literal['dict', 'list'] = 'dict',
    ):
        super().__init__(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            max_retries=max_retries,
            is_need_structured_output=is_need_structured_output,
            schema_pydantic_base_model=schema_pydantic_base_model,
            schema_check_type=schema_check_type,
        )
        logger.debug(f"Created NE Base Agent.")

    async def a_get_agent_response(
        self,
        chat_history: list[AnyMessage],
    ) -> AgentResponse:
        response = await self.a_call_llm_with_retry(
            chat_history=chat_history,
        )
        structured_output = self.get_structured_output(
            raw_str=response.content,
        )
        return AgentResponse(
            ai_message=response,
            structured_output=structured_output,
        )

