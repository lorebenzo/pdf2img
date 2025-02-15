FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y curl gcc libpq-dev poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# add poetry to the path variable
ENV PATH="/root/.local/bin:$PATH"

# copy and install the dependencies
COPY pyproject.toml poetry.lock ./

# do not create v_envs since we are not in a development scenario
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "pdf_be.app:app",  "--port", "8000", "--host", "0.0.0.0"]