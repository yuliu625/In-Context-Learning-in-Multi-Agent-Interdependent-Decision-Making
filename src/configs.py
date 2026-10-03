from __future__ import annotations
from loguru import logger

from pydantic_settings import BaseSettings

import os
from dotenv import load_dotenv

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


load_dotenv()


# Runtime
IS_BATCH_CALL = os.getenv("IS_BATCH_CALL", "True").lower() in ("true", "1",)
MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "50"))


# Agents
FORMAT_MAX_RETRIES = int(os.getenv("FORMAT_MAX_RETRIES", "100"))

