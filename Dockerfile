FROM ghcr.io/astral-sh/uv:debian
workdir /app

copy pyproject.toml uv.lock ./
run uv sync --frozen --no-install-project

copy . .

RUN uv sync --frozen
cmd ["uv", "run", "main"]