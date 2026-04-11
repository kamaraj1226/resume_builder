FROM ghcr.io/astral-sh/uv:debian
workdir /resume_builder

copy pyproject.toml uv.lock ./
run uv sync --frozen --no-install-project

copy . .
cmd ["uv", "run", "main"]