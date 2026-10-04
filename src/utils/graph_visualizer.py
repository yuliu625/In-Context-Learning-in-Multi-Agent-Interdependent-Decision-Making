from __future__ import annotations
from loguru import logger

from IPython.display import Image, display

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from langgraph.graph.state import CompiledStateGraph


class GraphVisualizer:
    @staticmethod
    def get_mermaid_code(
        graph: CompiledStateGraph,
    ) -> str:
        mermaid_code = graph.get_graph().draw_mermaid()
        logger.info(f"Mermaid Code: \n{mermaid_code}")
        return mermaid_code

    @staticmethod
    def get_mermaid_png(
        graph: CompiledStateGraph,
    ) -> Image:
        mermaid_png = Image(graph.get_graph().draw_mermaid_png())
        display(mermaid_png)
        return mermaid_png

    @staticmethod
    def save_mermaid_png(
        graph: CompiledStateGraph,
        output_file_path: str,
    ) -> Image:
        mermaid_png = Image(
            graph.get_graph().draw_mermaid_png(
                output_file_path=output_file_path,
            ),
        )
        return mermaid_png

