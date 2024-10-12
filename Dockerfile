FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --no-cache --no-dev

CMD ["/app/.venv/bin/uvicorn", "--factory", "--host", "0.0.0.0", "--port", "80", "src.main:create_application"]
