FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /workspace

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

