FROM python:3.11.10-slim-bookworm AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN echo 'Acquire::http::Pipeline-Depth 0;\nAcquire::http::No-Cache true;\nAcquire::BrokenProxy true;\n' > /etc/apt/apt.conf.d/99fixbadproxy

##############国内镜像源设置######################
RUN apt-get update && apt-get install -y gnupg2
COPY autogpt_platform/backend/sources.list /etc/apt/sources.list
# Update package list and install build dependencies in a single layer
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 871920D1991BC93C \
    && apt-get update --allow-releaseinfo-change --fix-missing \
    && apt-get install -y \
    build-essential \
    libpq5 \
    libz-dev \
    libssl-dev \
    postgresql-client \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME=/opt/poetry
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH=/opt/poetry/bin:$PATH

# Upgrade pip and setuptools to fix security vulnerabilities
# RUN pip3 install --upgrade pip setuptools

# RUN pip3 install poetry

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip3 install --upgrade pip setuptools \ 
    && pip3 install poetry

# Copy and install dependencies
COPY autogpt_platform/autogpt_libs /app/autogpt_platform/autogpt_libs
COPY autogpt_platform/backend/poetry.lock autogpt_platform/backend/pyproject.toml /app/autogpt_platform/backend/
WORKDIR /app/autogpt_platform/backend

RUN poetry source add aliyun https://mirrors.aliyun.com/pypi/simple/ --priority=primary \
    && poetry update && poetry install --no-ansi --no-root 
# RUN poetry install --no-ansi --no-root

# Generate Prisma client
COPY autogpt_platform/backend/schema.prisma ./

RUN npm config set registry https://registry.npmmirror.com \
    && npm install -g n \
    && n stable \
    && npm install npm@latest -g
RUN poetry run prisma generate

FROM python:3.11.10-slim-bookworm AS server_dependencies

WORKDIR /app

ENV POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false
ENV PATH=/opt/poetry/bin:$PATH

# Upgrade pip and setuptools to fix security vulnerabilities
# RUN pip3 install --upgrade pip setuptools
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip3 install --upgrade pip setuptools

# Copy only necessary files from builder
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
# Copy Prisma binaries
COPY --from=builder /root/.cache/prisma-python/binaries /root/.cache/prisma-python/binaries


ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p /app/autogpt_platform/autogpt_libs
RUN mkdir -p /app/autogpt_platform/backend

COPY autogpt_platform/autogpt_libs /app/autogpt_platform/autogpt_libs

COPY autogpt_platform/backend/poetry.lock autogpt_platform/backend/pyproject.toml /app/autogpt_platform/backend/

WORKDIR /app/autogpt_platform/backend

FROM server_dependencies AS migrate

# Migration stage only needs schema and migrations - much lighter than full backend
COPY autogpt_platform/backend/schema.prisma /app/autogpt_platform/backend/
COPY autogpt_platform/backend/migrations /app/autogpt_platform/backend/migrations

FROM server_dependencies AS server

COPY autogpt_platform/backend /app/autogpt_platform/backend
# RUN poetry install --no-ansi --only-root
RUN poetry source add aliyun https://mirrors.aliyun.com/pypi/simple/ --priority=primary \
    && poetry update && poetry install --no-ansi --only-root

ENV PORT=8000

CMD ["poetry", "run", "rest"]
