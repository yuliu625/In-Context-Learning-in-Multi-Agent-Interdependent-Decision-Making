from __future__ import annotations
import pytest
from loguru import logger

from pathlib import Path

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


@pytest.fixture(name='data_dir',)
def get_data_dir() -> Path:
    return Path(__file__).parent / "data"

