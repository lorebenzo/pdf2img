FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# add poetry to the path variable
ENV PATH="/root/.local/bin:$PATH"

# copy and install the dependencies
COPY pyproject.toml poetry.lock ./

# do not create v_envs since we are not in a development scenario
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# copy the application
COPY . .

EXPOSE 8501

ENTRYPOINT ["poetry", "run", "streamlit", "run", \
     "pdf_fe/app.py", \
     "--server.port=8501", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]